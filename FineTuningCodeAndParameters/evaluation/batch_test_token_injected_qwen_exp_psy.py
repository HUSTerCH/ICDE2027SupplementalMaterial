# Run from FineTuningCodeAndParameters/.
# Supply --test_dataset, --adapter, and --output for the experiment to evaluate.
from unsloth import FastLanguageModel
import numpy as np
import random
import torch
from transformers import set_seed

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
set_seed(seed)

import argparse
import os
import json
import yaml

from peft import PeftModel
from tqdm import tqdm

STAGES = ["drainage", "induction", "transfer"]

parser = argparse.ArgumentParser(description="LoRA 批量推理与评估（三阶段被利用心理机制，基座模型已注入 token）")
parser.add_argument(
    "--config", "-c", type=str, default="configs/psychological_factor.yaml",
    help="训练配置文件路径（包含 model, env, training 等）"
)
parser.add_argument(
    "--test_dataset", "-t", type=str, default=None,
    help="测试集 JSON 文件路径"
)
parser.add_argument(
    "--adapter", "-a", type=str, required=True,
    help="LoRA adapter 权重目录（必需）"
)
parser.add_argument(
    "--output", "-o", type=str, default="batch_results_psychology.json",
    help="输出结果 JSON 文件路径"
)
parser.add_argument(
    "--batch_size", "-b", type=int, default=16,
    help="批量推理的 batch size"
)
parser.add_argument(
    "--max_new_tokens", '-mnt', type=int, default=4096,
    help="生成的最大 token 数"
)
args = parser.parse_args()

with open(args.config, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

env_cfg = cfg.get("env", {})
os.environ["HF_HUB_OFFLINE"] = "1"
if "hf_endpoint" in env_cfg:
    os.environ["HF_ENDPOINT"] = env_cfg["hf_endpoint"]

model_cfg = cfg["model"]
dtype = getattr(torch, model_cfg.get("dtype", "bfloat16"))
base_model_name = model_cfg["model_name"]

test_dataset_path = args.test_dataset
if not test_dataset_path or not os.path.exists(test_dataset_path):
    raise FileNotFoundError(f"测试数据集未找到: {test_dataset_path}")

def strip_code_fence(json_str: str) -> str:
    clean_str = json_str.strip()
    if clean_str.startswith("```json"):
        clean_str = clean_str[7:]
    if clean_str.startswith("```"):
        clean_str = clean_str[3:]
    if clean_str.endswith("```"):
        clean_str = clean_str[:-3]
    return clean_str.strip()

def extract_stage_labels_from_json_string(json_str: str):
    """提取三个阶段的标签；缺少任一阶段或 labels 列表时返回 None。"""
    try:
        clean_str = strip_code_fence(json_str)
        data = json.loads(clean_str)
        if not isinstance(data, dict):
            return None

        result = {}
        for stage in STAGES:
            info = data.get(stage)
            if not isinstance(info, dict) or "labels" not in info:
                return None
            labels = info.get("labels", [])
            if not isinstance(labels, list):
                return None
            result[stage] = labels
        return result
    except Exception:
        return None

def compare_stage_labels(pred_stage_labels, true_stage_labels):
    """逐阶段比较标签集合；无法解析的输入均视为不匹配。"""
    if pred_stage_labels is None or true_stage_labels is None:
        return {stage: False for stage in STAGES}
    return {
        stage: set(pred_stage_labels.get(stage, [])) == set(true_stage_labels.get(stage, []))
        for stage in STAGES
    }

print(f"加载基座模型: {base_model_name}")
model, processor = FastLanguageModel.from_pretrained(
    model_name=base_model_name,
    dtype=dtype,
    load_in_4bit=model_cfg.get("load_in_4bit", False),
    local_files_only=True,
)
try:
    tokenizer = processor.tokenizer
except AttributeError:
    tokenizer = processor
tokenizer.padding_side = "left"  # 批量生成使用左侧 padding。
print(f"词汇表大小: {len(tokenizer)}")

adapter_path = args.adapter
print(f"加载 LoRA 适配器: {adapter_path}")
model = PeftModel.from_pretrained(model, adapter_path)
print("LoRA 加载完成")

FastLanguageModel.for_inference(model)

stop_token_ids = [tokenizer.convert_tokens_to_ids("<|im_end|>")]
if tokenizer.eos_token_id:
    stop_token_ids.append(tokenizer.eos_token_id)

with open(test_dataset_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)
print(f"共读取到 {len(dataset)} 条测试数据")

all_samples = []
for i, sample in enumerate(dataset):
    messages = []
    true_stage_labels = None
    user_input = ""
    for turn in sample["conversations"]:
        if turn["from"] == "system":
            messages.append({"role": "system", "content": turn["value"]})
        elif turn["from"] == "human":
            messages.append({"role": "user", "content": turn["value"]})
            user_input = turn["value"]
        elif turn["from"] == "gpt":
            true_stage_labels = extract_stage_labels_from_json_string(turn["value"])
            break
    all_samples.append((i, messages, user_input, true_stage_labels))

valid_samples = [s for s in all_samples if s[3] is not None]
print(f"其中真实标签有效样本数: {len(valid_samples)} / {len(dataset)}")

results = []
BATCH_SIZE = args.batch_size
MAX_NEW_TOKENS = args.max_new_tokens

for batch_start in tqdm(range(0, len(all_samples), BATCH_SIZE), desc="批量推理进度"):
    batch = all_samples[batch_start: batch_start + BATCH_SIZE]

    texts = []
    for _, messages, _, _ in batch:
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        texts.append(text)

    inputs = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=4096,
    ).to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            use_cache=True,
            temperature=0,
            do_sample=False,
            eos_token_id=stop_token_ids,
            pad_token_id=tokenizer.pad_token_id,
        )

    input_length = inputs["input_ids"].shape[1]

    for i, (idx, messages, user_input, true_stage_labels) in enumerate(batch):
        STRIP_TOKENS = ["<|im_end|>", "<|endoftext|>", "<|im_start|>"]
        final_response = tokenizer.decode(
            outputs[i][input_length:], skip_special_tokens=False
        )
        for t in STRIP_TOKENS:
            final_response = final_response.replace(t, "")
        final_response = final_response.strip()

        pred_stage_labels = extract_stage_labels_from_json_string(final_response)
        is_valid_json = pred_stage_labels is not None

        stage_matches = compare_stage_labels(pred_stage_labels, true_stage_labels)
        is_full_match = is_valid_json and true_stage_labels is not None and all(stage_matches.values())

        json_status = "成功" if is_valid_json else "失败"
        match_status = "✅ 全阶段匹配" if is_full_match else "❌ 不匹配"
        print(f"[Sample {idx:04d}] JSON解析: {json_status} | 标签比对: {match_status}")

        if not is_full_match and is_valid_json and true_stage_labels is not None:

            for stage in STAGES:
                if not stage_matches[stage]:
                    print(f"  |- [{stage}] 真实: {true_stage_labels.get(stage, [])}  预测: {pred_stage_labels.get(stage, [])}")

        results.append({
            "sample_index": idx,
            "input_prompt": user_input,
            "raw_model_output": final_response,
            "extracted_true_stage_labels": true_stage_labels,
            "extracted_pred_stage_labels": pred_stage_labels,
            "is_valid_json": is_valid_json,
            "stage_matches": stage_matches,
            "is_full_match": is_full_match,
        })

valid_true_samples = [r for r in results if r["extracted_true_stage_labels"] is not None]
total_valid = len(valid_true_samples)

if total_valid > 0:
    valid_json_count = sum(1 for r in valid_true_samples if r["is_valid_json"])
    full_match_count = sum(1 for r in valid_true_samples if r["is_full_match"])
    json_validity_rate = valid_json_count / total_valid * 100
    overall_accuracy = full_match_count / total_valid * 100

    # 阶段完全匹配率的分母仅包含 JSON 解析成功的样本。
    stage_accuracy = {}
    valid_json_samples = [r for r in valid_true_samples if r["is_valid_json"]]
    for stage in STAGES:
        if valid_json_samples:
            stage_correct = sum(1 for r in valid_json_samples if r["stage_matches"][stage])
            stage_accuracy[stage] = stage_correct / len(valid_json_samples) * 100
        else:
            stage_accuracy[stage] = 0.0
else:
    valid_json_count = 0
    full_match_count = 0
    json_validity_rate = 0.0
    overall_accuracy = 0.0
    stage_accuracy = {stage: 0.0 for stage in STAGES}

summary = {
    "total_samples_in_dataset": len(dataset),
    "samples_with_valid_true_labels": total_valid,
    "valid_json_outputs_among_valid_true": valid_json_count,
    "full_stage_matches_among_valid_true": full_match_count,
    "json_validity_rate": f"{json_validity_rate:.2f}%",
    "overall_accuracy_all_3_stages": f"{overall_accuracy:.2f}%",
    "stage_accuracy": {stage: f"{acc:.2f}%" for stage, acc in stage_accuracy.items()},
}

final_output = {
    "summary": summary,
    "details": sorted(results, key=lambda x: x["sample_index"]),
}

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)

print("\n================ 测试完成 ================")
print(f"数据集总样本数: {summary['total_samples_in_dataset']}")
print(f"真实标签有效的样本数: {summary['samples_with_valid_true_labels']}")
print(f"有效样本中 JSON 格式合法率: {summary['json_validity_rate']}")
print(f"有效样本中三阶段全匹配率: {summary['overall_accuracy_all_3_stages']}")
for stage in STAGES:
    print(f"  [{stage}] 阶段精确匹配率: {summary['stage_accuracy'][stage]}")
print(f"详细结果已保存至: {args.output}")
