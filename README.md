# Supplemental Material

This repository accompanies our study of Chinese telecom scam cases. The study organizes case narratives into four stages—Attraction, Inducement, Transfer, and Awakening—and analyzes scam types, exploited psychological factors, and awakening factors.

The materials include CCL-derived large-scale analysis data, classification taxonomies, Chinese prompts with English translations, and code and configurations for task-specific LoRA fine-tuning. Model weights are available through the download link below.

## Repository Contents

| Directory | Contents |
|---|---|
| [Datasets/CCL](Datasets/CCL/README.md) | Large-scale analysis records, their data manifest, and a data-loading helper. |
| [FineTuningCodeAndParameters](FineTuningCodeAndParameters/) | Token Injection, weighted fine-tuning, task configurations, and batch evaluation scripts. |
| [Taxonomies](Taxonomies/) | Chinese and English category definitions for the three analysis tasks. |
| [prompts](prompts/readme.md) | Fine-tuning and baseline classification prompts, plus the CCL four-stage segmentation prompt. |

## Datasets

### Data_CCL

The released CCL-derived data support large-scale case analysis.

- `analysis/cases.jsonl.gz` contains 28,591 case records with four-stage narratives, financial losses, task eligibility information, and model predictions. The analysis labels are model outputs rather than manual ground truth.
- `manifest.json` records the analysis file's provenance, record counts, and fields.
- `read_data.py` reads the compressed analysis records directly with the Python standard library.

[The dataset guide](Datasets/CCL/README.md) explains the record fields and provides a reading example.

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

Before training, prepare compatible training data and update `model.model_name` to the downloaded token-injected model directory and `dataset.data_files` to your training JSON file; the dataset paths in the configurations are examples. Training examples use a `conversations` field, with `from` and `value` keys in each message. Include the original `weight` field when applying sample weighting.

After preparing the training data and updating the paths, a scam-type training run can be started from the repository root with:

```bash
cd FineTuningCodeAndParameters
python train_token_injected_qwen.py --config configs/scam_type.yaml
```

For evaluation, use `batch_test_token_injected_qwen.py` for scam types or awakening factors, and `batch_test_token_injected_qwen_exp_psy.py` for the three-stage psychological-factor task. Supply the matching configuration, adapter directory, and test file through `--config`, `--adapter`, and `--test_dataset`. Provide a compatible evaluation file separately in uncompressed JSON format. They export per-case predictions and report JSON validity and label exact-match accuracy.

## Model Downloads

The model files are available on [Google Drive](https://drive.google.com/drive/folders/1Gz10sBKE-vQz03Iy6PhAdnJvA2PNJwSI?usp=sharing).

The shared folder contains:

- One Qwen3.5-9B model extended with task-specific label tokens through Token Injection.
- Three fine-tuned LoRA adapters, one for each classification task:
  - Scam-type classification.
  - Exploited psychological factor classification.
  - Awakening factor classification.

Use the LoRA adapters with the token-injected Qwen3.5-9B model provided in the same folder.
