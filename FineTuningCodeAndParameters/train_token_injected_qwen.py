"""对 Token 注入后的模型进行加权 LoRA 微调。
用法：python train_token_injected_qwen.py --config configs/scam_type.yaml
"""
import faulthandler; faulthandler.enable()
import argparse
import os
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
from datetime import datetime
from unsloth import FastLanguageModel
import torch
import yaml
from datasets import load_dataset, load_from_disk
from trl import SFTConfig, SFTTrainer

from weighted_trainer import WeightedDataCollator, WeightedTrainer

ROLE_MAPPING = {
    "human": "user",
    "gpt": "assistant",
    "assistant": "assistant",
    "model": "assistant",
    "bot": "assistant",
    "system": "system",
}
print("启动脚本train_token_injected_qwen.py")

def formatting_prompts_func(examples):
    convos = examples["conversations"]
    # 缺少样本权重时使用 1.0。
    weight = examples.get("weight", [1.0] * len(convos))
    texts = []
    for convo in convos:
        standard_convo = []
        for msg in convo:
            raw_role = msg.get("from", "").lower()
            safe_role = ROLE_MAPPING.get(raw_role, "user")
            standard_convo.append({"role": safe_role, "content": msg["value"]})
        text = real_tokenizer.apply_chat_template(
            standard_convo, tokenize=False, add_generation_prompt=False
        )
        texts.append(text)
    return {"text": texts, "weight": weight}

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="")
parser.add_argument("--resume", type=str, default=None, help="断点续训 checkpoint 路径")
args = parser.parse_args()

with open(args.config, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

env_cfg = cfg["env"]
os.environ["HF_ENDPOINT"] = env_cfg["hf_endpoint"]
os.environ["WANDB_DISABLED"] = env_cfg["wandb_disabled"]

model_cfg = cfg["model"]
lora_cfg = cfg["lora"]
dataset_cfg = cfg["dataset"]
train_cfg = cfg["training"]
fl_cfg = cfg["focal_loss"]

_DTYPE_MAP = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
}
dtype = _DTYPE_MAP[model_cfg["dtype"]]

injected_model_path = cfg.get("injected_model_path", model_cfg["model_name"])
print(f"Loading injected model from {injected_model_path} ...")

model, processor = FastLanguageModel.from_pretrained(
    model_name=injected_model_path,
    max_seq_length=model_cfg["max_seq_length"],
    dtype=dtype,
    load_in_4bit=model_cfg["load_in_4bit"],
    local_files_only=model_cfg.get("local_files_only", False),
)
try:
    real_tokenizer = processor.tokenizer
except AttributeError:
    real_tokenizer = processor

# Token 已在基座中注入，此处不再扩充词表。

model = FastLanguageModel.get_peft_model(
    model,
    r=lora_cfg["r"],
    target_modules=lora_cfg["target_modules"],
    modules_to_save=lora_cfg["modules_to_save"],
    lora_alpha=lora_cfg["lora_alpha"],
    lora_dropout=lora_cfg["lora_dropout"],
    bias=lora_cfg["bias"],
    use_gradient_checkpointing=lora_cfg["use_gradient_checkpointing"],
    random_state=lora_cfg["random_state"],
)

# 兼容扩充词表后的 PEFT 保存逻辑。
model.peft_config["default"].save_embedding_layers = True
new_vocab_size = len(real_tokenizer)
if not hasattr(model.config.__class__, "vocab_size"):
    setattr(model.config.__class__, "vocab_size", new_vocab_size)

actual_vocab = model.get_input_embeddings().weight.shape[0]
print(f"tokenizer len = {len(real_tokenizer)}, embedding rows = {actual_vocab}")
assert len(real_tokenizer) <= actual_vocab, "tokenizer 词表比 embedding 矩阵还大，会越界！"

# 同时训练特殊 token 的嵌入和输出层，并随适配器保存。
model.get_input_embeddings().requires_grad_(True)
model.get_output_embeddings().requires_grad_(True)

dataset = load_dataset("json", data_files=dataset_cfg["data_files"], split=dataset_cfg["split"])
dataset = dataset.map(formatting_prompts_func, batched=True)

print(f"训练数据集有 {len(dataset)} 条数据")

now = datetime.now()
time_format = now.strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(train_cfg["output_dir_base"], f"checkpoint_{time_format}")

extra_save_kwargs = {}
if train_cfg["save_strategy"] == "steps" and train_cfg.get("save_steps"):
    extra_save_kwargs["save_steps"] = train_cfg["save_steps"]

sft_config = SFTConfig(
    per_device_train_batch_size=train_cfg["per_device_train_batch_size"],
    gradient_accumulation_steps=train_cfg["gradient_accumulation_steps"],
    warmup_ratio=train_cfg["warmup_ratio"],
    num_train_epochs=train_cfg["num_train_epochs"],
    save_strategy=train_cfg["save_strategy"],
    save_total_limit=train_cfg["save_total_limit"],
    learning_rate=train_cfg["learning_rate"],
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=train_cfg["logging_steps"],
    optim=train_cfg["optim"],
    weight_decay=train_cfg["weight_decay"],
    lr_scheduler_type=train_cfg["lr_scheduler_type"],
    seed=train_cfg["seed"],
    output_dir=output_dir,
    dataset_text_field=train_cfg["dataset_text_field"],
    max_length=model_cfg["max_seq_length"],
    dataset_num_proc=dataset_cfg["dataset_num_proc"],
    packing=train_cfg["packing"],
    remove_unused_columns=False,
    **extra_save_kwargs,
)

data_collator = WeightedDataCollator(tokenizer=real_tokenizer, mlm=False)
trainer = WeightedTrainer(
    use_focal_loss=fl_cfg.get("enabled", False),
    gamma=fl_cfg.get("gamma", 2.0),
    model=model,
    processing_class=processor,
    train_dataset=dataset,
    args=sft_config,
    data_collator=data_collator,
)

if args.resume:
    trainer.train(resume_from_checkpoint=args.resume)
else:
    trainer.train()
