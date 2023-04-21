import os
import time

from .base import ScoreListener


class ScoreRecorder(ScoreListener):
    path: str

    def __init__(self, path: str):
        self.path = path
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def handle(self, prompt_name: str, model_name: str, score: float) -> None:
        with open(self.path, "a") as f:
            # format yyyy-mm-dd hh:mm:ss
            t = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
            f.write(f"{t},{prompt_name},{model_name},{score}\n")
