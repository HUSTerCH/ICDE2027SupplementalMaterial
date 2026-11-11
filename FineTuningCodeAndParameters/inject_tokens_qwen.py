# Run from FineTuningCodeAndParameters/. Update the model paths below.

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["WANDB_DISABLED"] = "true"
from unsloth import FastLanguageModel

from new_tokens import new_tokens_need_add

BASE_MODEL_NAME = "../models/Qwen3.5-9B"

LOAD_IN_4BIT = False
DTYPE = "bfloat16"

# 将扩充后的嵌入矩阵行数对齐到该倍数。
PAD_TO_MULTIPLE = 8

OUTPUT_DIR = "../models/Qwen3.5-9B-Token-Injected"

def main():
    print(f"Loading base model: {BASE_MODEL_NAME}")
    model, processor = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL_NAME,
        dtype=DTYPE,
        load_in_4bit=LOAD_IN_4BIT,
    )
    # 兼容返回 tokenizer 或 processor 的 Unsloth 版本。
    try:
        tokenizer = processor.tokenizer
    except AttributeError:
        tokenizer = processor

    print("Adding special tokens...")
    num_added = tokenizer.add_special_tokens({"additional_special_tokens": new_tokens_need_add})
    print(f"Added {num_added} tokens, new vocab size: {len(tokenizer)}")

    model.resize_token_embeddings(
        len(tokenizer),
        pad_to_multiple_of=PAD_TO_MULTIPLE
    )
    model.config.vocab_size = len(tokenizer)

    # 同步生成配置中的词表大小。
    if hasattr(model, "generation_config"):
        model.generation_config.vocab_size = len(tokenizer)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Saving injected model to {OUTPUT_DIR} ...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Done.")

if __name__ == "__main__":
    main()
