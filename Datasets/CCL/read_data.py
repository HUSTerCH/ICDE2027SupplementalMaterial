"""Read the released CCL analysis records using only the Python standard library."""

import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def iter_analysis_cases():
    # Read one complete JSON record at a time to keep memory usage low.
    with gzip.open(ROOT / 'analysis/cases.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


if __name__ == '__main__':
    print('Analysis records:', sum(1 for _ in iter_analysis_cases()))
