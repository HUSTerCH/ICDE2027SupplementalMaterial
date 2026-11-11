# Supplemental Material

This repository accompanies our study of Chinese telecom scam cases. The study organizes case narratives into four stages—Attraction, Inducement, Transfer, and Awakening—and analyzes scam types, exploited psychological factors, and awakening factors.

The materials include CCL-derived data, classification taxonomies, Chinese prompts with English translations, and code and configurations for task-specific LoRA fine-tuning. Model weights are available through the download link below.

## Repository Contents

| Directory | Contents |
|---|---|
| [Datasets/CCL](Datasets/CCL/README.md) | Training and evaluation examples, large-scale analysis records, and a data-loading helper. |
| [FineTuningCodeAndParameters](FineTuningCodeAndParameters/) | Token Injection, weighted fine-tuning, task configurations, and batch evaluation scripts. |
| [Taxonomies](Taxonomies/) | Chinese and English category definitions for the three analysis tasks. |
| [prompts](prompts/readme.md) | Fine-tuning and baseline classification prompts, plus the CCL four-stage segmentation prompt. |

## Datasets

### Data_CCL

The released CCL-derived data cover the three classification tasks and large-scale case analysis:

- `training_and_evaluation/` contains a separate folder for each task. Each folder provides `train.json.gz`, `test.json.gz`, and `baseline_test.json.gz`. Each task has 1,000 evaluation cases; the two test formats contain the same case IDs.
- `analysis/cases.jsonl.gz` contains 28,591 case records with four-stage narratives, financial losses, task eligibility information, and model predictions. The analysis labels are model outputs rather than manual ground truth.
- `manifest.json` records the source versions and exported record counts. Training exports include augmented examples and may contain repetitions, so their sizes should not be interpreted as counts of distinct manually annotated real cases.

The files are gzip-compressed. [The dataset guide](Datasets/CCL/README.md) explains their fields and provides examples using `read_data.py`, which reads the compressed files directly with the Python standard library.

### Data_INT

Data_INT consists of scam cases extracted from public online reports. It is not included in the current release and is planned for release after paper acceptance.

## Taxonomies and Prompts

The taxonomies define the labels used in the study:

- **Scam types:** 6 top-level categories and 18 fine-grained subcategories; a case may contain multiple scam types.
- **Psychological factors:** 8 psychological categories and a supplementary category for non-cognitive technical attacks, analyzed across Attraction, Inducement, and Transfer.
- **Awakening factors:** 8 categories describing factors associated with scam recognition or termination.

Each taxonomy is provided in Chinese and English under [Taxonomies](Taxonomies/).

The [prompts directory](prompts/readme.md) separates fine-tuning/fine-tuned-model prompts from baseline prompts. Each version includes shared system instructions and task-specific files. The preprocessing folder contains the CCL four-stage segmentation prompt. Chinese files retain the original prompt text; English files are reference translations and do not represent a separately evaluated English-language setting.

## Fine-Tuning and Evaluation

The code under [FineTuningCodeAndParameters](FineTuningCodeAndParameters/) includes:

- `inject_tokens_qwen.py` and `new_tokens.py`: extend the base model with task-specific label tokens.
- `train_token_injected_qwen.py` and `weighted_trainer.py`: perform LoRA fine-tuning using the sample weights in the training records.
- `configs/`: provide a separate training configuration for each task.
- `evaluation/`: run batch inference with a trained adapter and save predictions and evaluation summaries.

| Task | Configuration |
|---|---|
| Scam-type classification | [scam_type.yaml](FineTuningCodeAndParameters/configs/scam_type.yaml) |
| Psychological-factor classification | [psychological_factor.yaml](FineTuningCodeAndParameters/configs/psychological_factor.yaml) |
| Awakening-factor classification | [awakening_factor.yaml](FineTuningCodeAndParameters/configs/awakening_factor.yaml) |

Dependencies are listed in [requirements.txt](FineTuningCodeAndParameters/requirements.txt). The original training environment used CUDA-enabled PyTorch; install a build suitable for the training machine.

Before training, update `model.model_name` to the downloaded token-injected model directory and `dataset.data_files` to the corresponding training file. For example, when running from `FineTuningCodeAndParameters/`, the released scam-type training file is `../Datasets/CCL/training_and_evaluation/scam_type/train.json.gz`. Retain the original sample weights.

After updating the paths, a scam-type training run can be started from the repository root with:

```bash
cd FineTuningCodeAndParameters
python train_token_injected_qwen.py --config configs/scam_type.yaml
```

For evaluation, use `batch_test_token_injected_qwen.py` for scam types or awakening factors, and `batch_test_token_injected_qwen_exp_psy.py` for the three-stage psychological-factor task. Supply the matching configuration, adapter directory, and test file through `--config`, `--adapter`, and `--test_dataset`. These scripts read uncompressed JSON, so decompress the relevant `test.json.gz` before running them. They export per-case predictions and report JSON validity and label exact-match accuracy.

## Model Downloads

The model files are available on [Google Drive](https://drive.google.com/drive/folders/1Gz10sBKE-vQz03Iy6PhAdnJvA2PNJwSI?usp=sharing).

The shared folder contains:

- One Qwen3.5-9B model extended with task-specific label tokens through Token Injection.
- Three fine-tuned LoRA adapters, one for each classification task:
  - Scam-type classification.
  - Exploited psychological factor classification.
  - Awakening factor classification.

Use the LoRA adapters with the token-injected Qwen3.5-9B model provided in the same folder.
