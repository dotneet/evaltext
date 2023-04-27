from dataclasses import dataclass
import logging
import math
import time
from abc import ABC, abstractmethod
from typing import List

class GenerationListener(ABC):
    @abstractmethod
    def handle(self, prompt: str, prompt_name: str, model_name: str, response: str, elapsed: float,
               score: float) -> None:
        pass

class GenerationConsoleOutputListener(GenerationListener):

    verbose: bool

    def __init__(self, verbose:bool=False) -> None:
        self.verbose = verbose

    def handle(self, prompt: str, prompt_name: str, model_name: str, response: str, elapsed: float,
               score: float) -> None:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        csv_row = ",".join([t, prompt_name, model_name, str(score), str(math.floor(elapsed * 10) / 10)])
        logging.log(logging.INFO, f"recorded: {csv_row}")
        if self.verbose:
            logging.log(logging.INFO, f"prompt: {prompt}")
            logging.log(logging.INFO, f"response: {response}")

@dataclass
class SamplingResult:
    response: str
    score: float
    elapsed: float

class ScoreListener(ABC):
    @abstractmethod
    def handle(self, prompt: str, prompt_name: str, model_name: str, results:List[SamplingResult]) -> None:
        pass
