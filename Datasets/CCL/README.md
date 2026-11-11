# Data_CCL

This directory provides the CCL-derived data used for model training, evaluation, and large-scale case analysis. Source versions and record counts are listed in `manifest.json`.

## Training and evaluation data

| Task | Training records | Test records | Source version |
| --- | ---: | ---: | --- |
| Scam-type classification | 4,609 | 1,000 | 0706 |
| Psychological factor classification | 4,836 | 1,000 | Training: 0801; evaluation: 0802 |
| Awakening factor classification | 3,541 | 1,000 | 0622 |

Each task folder under `training_and_evaluation/` contains:

- `train.json.gz`: the exported training examples, including their original sample weights.
- `test.json.gz`: evaluation examples in the fine-tuned model's format.
- `baseline_test.json.gz`: the same evaluation case IDs in the baseline evaluation format.

The files retain the original export bytes after decompression. Each JSON file contains a list of examples with `id` and `conversations` fields. Training exports also include `weight`. Conversation entries use the `from` and `value` keys. Original task tokens and label codes are preserved.

Training counts describe exported examples, including augmented examples and any repetitions already present in the selected export. They are not counts of newly annotated real cases. Within each task, training and test case IDs are disjoint.

## Large-scale analysis data

`analysis/cases.jsonl.gz` contains 28,591 case records. The awakening-factor analysis subset contains 21,901 records. The analysis case IDs do not overlap with the training or evaluation IDs of the three tasks.

The file uses JSON Lines, with one record per line:

| Field | Description |
| --- | --- |
| `id` | Case identifier used to join records. |
| `four_stages` | The four-stage case narrative, stored as a JSON string. |
| `data_suitable` | Task eligibility information, stored as a JSON string. |
| `total_loss` | Financial loss in CNY. |
| `fraud_typology_eval_result` | Original scam-type model prediction. |
| `exploited_psychology_eval_result` | Original psychological factor model prediction. |
| `awakening_factors_eval_result` | Original awakening-factor model prediction, or null when unavailable. |

The analysis labels are model predictions, not manual ground truth. Nested JSON strings and model responses retain their source representations. A JSON parser should be used with error handling when reading these fields. Historical field names are retained for compatibility with the analysis code.

## Reading the files

All data files are gzip-compressed. They can be read directly with the Python standard library; no extraction tool or additional package is required.

```python
import json
from read_data import load_task_data, iter_analysis_cases

test_cases = load_task_data("scam_type", "test")
train_cases = load_task_data("psychological_factors", "train")

for case in iter_analysis_cases():
    stages = json.loads(case["four_stages"])
    loss = case["total_loss"]
    # Process the case without loading the entire analysis file into memory.
```

Available task names are `scam_type`, `psychological_factors`, and `awakening_factors`. Available splits are `train`, `test`, and `baseline_test`.

Run `python read_data.py` for a basic loading check. The files can also be decompressed using any standard gzip tool.
