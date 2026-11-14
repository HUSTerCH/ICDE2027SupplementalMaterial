# Data_CCL

This directory provides CCL-derived case records used for large-scale analysis.

## Available files

- `analysis/cases.jsonl.gz`: gzip-compressed case records in JSON Lines format.
- `manifest.json`: file provenance, record counts, and field information.
- `read_data.py`: a helper for reading the analysis records with the Python standard library.

## Large-scale analysis data

`analysis/cases.jsonl.gz` contains 28,591 case records. The awakening-factor analysis subset contains 21,901 records.

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

## Reading the data

The analysis file can be read directly without decompression or additional packages. From this directory, use:

```python
import json
from read_data import iter_analysis_cases

for case in iter_analysis_cases():
    stages = json.loads(case["four_stages"])
    loss = case["total_loss"]
    # Process each case without loading the entire file into memory.
```

Run `python read_data.py` from this directory for a basic loading check. The file can also be decompressed using any standard gzip tool.
