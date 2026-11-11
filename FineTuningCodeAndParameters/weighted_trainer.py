from trl import SFTTrainer
import torch
from transformers import DataCollatorForLanguageModeling

class WeightedDataCollator(DataCollatorForLanguageModeling):
    def __call__(self, features, return_tensors=None):
        # 保留样本权重，避免默认 collator 丢弃该字段。
        weights = [feature.pop("weight", 1.0) for feature in features]
        batch = super().__call__(features, return_tensors)
        batch["weight"] = torch.tensor(weights, dtype=torch.float32)
        return batch

class WeightedTrainer(SFTTrainer):
    def __init__(self, use_focal_loss=False, gamma=2.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_focal_loss = use_focal_loss
        self.gamma = gamma

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        # 权重仅用于计算损失，不传给模型 forward。
        sample_weights = inputs.pop("weight", None)
        if sample_weights is not None:
            sample_weights = sample_weights.view(-1).to(model.device)

        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")

        # 对齐下一 token 的预测与真实标签。
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        shift_logits_view = shift_logits.view(-1, shift_logits.size(-1))
        shift_labels_view = shift_labels.view(-1)

        loss_fct = torch.nn.CrossEntropyLoss(reduction="none")
        token_losses = loss_fct(shift_logits_view, shift_labels_view)

        # 可选的 Focal Loss。
        if self.use_focal_loss:
            pt = torch.exp(-token_losses)
            token_losses = (((1 - pt) ** self.gamma) * token_losses)

        token_losses = token_losses.view(shift_labels.size(0), -1)

        # 忽略标签为 -100 的位置。
        valid_mask = (shift_labels != -100)
        valid_losses = token_losses * valid_mask

        # 先按每个样本的有效 token 数求平均，再应用样本权重。
        seq_loss = valid_losses.sum(dim=1) / valid_mask.float().sum(dim=1).clamp(min=1e-6)

        if sample_weights is not None:
            seq_loss = seq_loss * sample_weights

        loss = seq_loss.mean()

        return (loss, outputs) if return_outputs else loss
