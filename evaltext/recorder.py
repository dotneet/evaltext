import fcntl
import json
import logging
import math
import os
import time
import numpy as np
from typing import List

from .base import SamplingResult, ScoreListener


class ScoreRecorder(ScoreListener):
    path: str
    verbose: bool

    def __init__(self, path: str, verbose:bool=False):
        self.path = path
        self.verbose = verbose
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def handle(self, prompt: str, prompt_name: str, model_name: str, results: List[SamplingResult]) -> None:
        score_mean = math.floor(np.mean([r.score for r in results]) * 10) / 10
        elapsed_mean = math.floor(np.mean([r.elapsed for r in results]) * 10) / 10
        with open(self.path, "a") as f:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            record = {
                "time": t,
                "prompt_name": prompt_name,
                "model_name": model_name,
                "score": score_mean * 10,
                "prompt": prompt,
                "response": results[0].response,
                "elapsed": elapsed_mean,
            }
            json_data = json.dumps(record)
            fcntl.lockf(f, fcntl.LOCK_EX)
            try:
                f.write(f"{json_data}\n")
            finally:
                fcntl.lockf(f, fcntl.LOCK_UN)

            if self.verbose:
                csv_row = ",".join([t, prompt_name, model_name, str(score_mean), str(elapsed_mean)])
                logging.log(logging.INFO, f"recorded: {csv_row}")
