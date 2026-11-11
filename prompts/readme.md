# Prompts

This directory contains prompts for four-stage case segmentation and three classification tasks: scam types, exploited psychological factors, and awakening factors.

The Chinese files reproduce the prompts used in the experiments. The English files are translations for reference. They do not represent a separately evaluated English-language setting. Label codes, JSON field names, stage keys, decision rules, and few-shot labels are retained in the translations.

## Classification Prompts

| Version | Chinese originals | English translations |
|---|---|---|
| Fine-tuning and fine-tuned-model inference | [zh-cn/fine_tuning/](zh-cn/fine_tuning/) | [en/fine_tuning/](en/fine_tuning/) |
| Baseline evaluation | [zh-cn/baseline/](zh-cn/baseline/) | [en/baseline/](en/baseline/) |

Each classification directory contains four files:

| File | Purpose |
|---|---|
| `system.txt` | Shared role, analysis workflow, and output instructions for that version. |
| `fraud_typology.txt` | Two-level, multi-label scam-type classification. |
| `exploited_psychology.txt` | Psychological-factor classification across Attraction, Inducement, and Transfer in one request. |
| `awakening_factors.txt` | Classification of factors associated with scam recognition or termination. |

## Four-Stage Segmentation

The CCL four-stage segmentation prompt is provided below. The Chinese file is extracted unchanged from the original prompt constant; the English file is a reference translation.

| Dataset | Chinese original | English translation |
|---|---|---|
| Data_CCL | [CCL segmentation prompt](zh-cn/preprocessing/four_stage_segmentation_ccl.txt) | [CCL segmentation prompt](en/preprocessing/four_stage_segmentation_ccl.txt) |

Use the prompt as the system message. The user message contains the original case narrative and any attachment descriptions.

The output contains `global_appendix` and `four_stages`. Stage keys are `drainage`, `induction`, `transfer`, and `awake`, corresponding to Attraction, Inducement, Transfer, and Awakening. Each stage contains `content` and `attached_evidence`.

The prompt specifies a fixed description for self-service cases without an Inducement stage.
