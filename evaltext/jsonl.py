import datetime
import json
from typing import Callable

import jsonlines
import matplotlib.pyplot as plt
import pandas as pd


def read_jsonl_records(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return [json.loads(line) for line in lines]


def read_jsonl_record(file_path: str, line_number: int):
    return read_jsonl_records(file_path)[line_number]


def eval_jsonl_item(file_path: str, line_number: int, scoring_fn: Callable[[str], float]):
    record = read_jsonl_record(file_path, line_number)['response']
    return scoring_fn(record['response'])

def plot_scores_by_model(file_path: str):
    data = []
    with jsonlines.open(file_path) as reader:
        for item in reader:
            data.append(item)

    df = pd.DataFrame(data)

    df['time'] = pd.to_datetime(df['time'])
    print(df)
    df['time'] = df['time'].apply(lambda x: x.strftime('%Y-%m-%d %H'))
    _, ax = plt.subplots()
    for name, group in df.groupby('model_name'):
        group.plot(x='time', y='score', ax=ax, label=name)

    plt.show()