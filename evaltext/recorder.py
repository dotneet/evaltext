import fcntl
import json
import logging
import math
import os
import time

from .base import ScoreListener


class ScoreRecorder(ScoreListener):
    path: str
    verbose: bool
    verbose_detail: bool

    def __init__(self, path: str, verbose=False, verbose_detail=False):
        self.path = path
        self.verbose = verbose
        self.verbose_detail = verbose_detail
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def handle(self, prompt: str, prompt_name: str, model_name: str, response: str, elapsed: float,
               score: float) -> None:
        with open(self.path, "a") as f:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            record = {
                "time": t,
                "prompt_name": prompt_name,
                "model_name": model_name,
                "score": score,
                "prompt": prompt,
                "response": response,
                "elapsed": math.floor(elapsed * 10) / 10,
            }
            json_data = json.dumps(record)
            fcntl.lockf(f, fcntl.LOCK_EX)
            try:
                f.write(f"{json_data}\n")
            finally:
                fcntl.lockf(f, fcntl.LOCK_UN)

            if self.verbose:
                csv_row = ",".join([t, prompt_name, model_name, str(score), str(math.floor(elapsed * 10) / 10)])
                logging.log(logging.INFO, f"recorded: {csv_row}")
            if self.verbose_detail:
                logging.log(logging.INFO, f"prompt: {prompt}")
                logging.log(logging.INFO, f"response: {response}")
