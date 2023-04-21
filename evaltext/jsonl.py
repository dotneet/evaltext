import json
from typing import Callable


def read_jsonl_records(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return [json.loads(line) for line in lines]


def read_jsonl_record(file_path: str, line_number: int):
    return read_jsonl_records(file_path)[line_number]


def eval_jsonl_item(file_path: str, line_number: int, scoring_fn: Callable[[str], float]):
    record = read_jsonl_record(file_path, line_number)['response']
    return scoring_fn(record['response'])
