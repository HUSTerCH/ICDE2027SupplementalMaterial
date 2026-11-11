"""Read the compressed CCL files using only the Python standard library."""

import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_task_data(task, split='test'):
    path = ROOT / 'training_and_evaluation' / task / (split + '.json.gz')
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        return json.load(stream)


def iter_analysis_cases():
    # The file is JSON Lines: one complete record on each line.
    with gzip.open(ROOT / 'analysis/cases.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


if __name__ == '__main__':
    print('Scam-type evaluation records:', len(load_task_data('scam_type')))
    print('Analysis records:', sum(1 for _ in iter_analysis_cases()))
