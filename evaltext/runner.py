import os
import time
import logging
from enum import Enum
from typing import List, Callable

from .generator import (CohereGenerator, OpenAiChatGenerator, OpenAiGenerator,
                        TextGenerator)


class ScoreStorage:
    path: str

    def __init__(self, path: str):
        self.path = path
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def handle(self, name: str, score: float):
        with open(self.path, "a") as f:
            # format yyyy-mm-dd hh:mm:ss
            t = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
            f.write(f"{t},{name},{score}\n")


class Runner:
    prompts_dir: str
    output_dir: str
    listener: ScoreStorage

    def __init__(self, generators: List[TextGenerator], listener: ScoreStorage):
        self.generators = generators
        self.listener = listener

    def measure(self, path: str, scorer: Callable[[str], float]) -> List[float]:
        with open(path, "r") as f:
            prompt = f.read()
            for gen in self.generators:
                logging.log(logging.INFO, f"measuring {path} - {gen.name}...")
                res = gen.generate(prompt)
                score = scorer(res)
                self.listener.handle(gen.name, score)


class GeneratorType(Enum):
    OPENAI_GPT4 = 'openai-gpt4'
    OPENAI_GPT_3_5_TURBO = 'openai-gpt-3.5-turbo'
    OPENAI_GPT_3_5_TURBO_0301 = 'openai-gpt-3.5-turbo-0301'
    OPENAI_DAVINCI_003 = 'openai-davinci-003'
    OPENAI_DAVINCI_002 = 'openai-davinci-002'
    COHERE_XLARGE = 'cohere-xlarge'
    COHERE_MEDIUM = 'cohere-medium'
    OPENAI_BABBAGE_001 = 'openai-babbage-001'


def create_runner(types: List[GeneratorType], prompts_dir: str = 'prompts',
                  output_path: str = 'output/score.csv') -> Runner:
    generators: List[TextGenerator] = []
    listener = ScoreStorage(output_path)
    for t in types:
        if t == GeneratorType.OPENAI_GPT_3_5_TURBO:
            generators.append(OpenAiChatGenerator({'model': 'gpt-3.5-turbo'}))
        elif t == GeneratorType.OPENAI_GPT_3_5_TURBO_0301:
            generators.append(OpenAiChatGenerator({'model': 'gpt-3.5-turbo-0301'}))
        elif t == GeneratorType.OPENAI_DAVINCI_003:
            generators.append(OpenAiGenerator({'model': 'text-davinci-003'}))
        elif t == GeneratorType.OPENAI_DAVINCI_002:
            generators.append(OpenAiGenerator({'model': 'text-davinci-002'}))
        elif t == GeneratorType.COHERE_XLARGE:
            generators.append(CohereGenerator({'model': 'xlarge'}))
        elif t == GeneratorType.COHERE_MEDIUM:
            generators.append(CohereGenerator({'model': 'medium'}))
        else:
            raise ValueError(f'Unknown generator type: {t}')
    return Runner(generators=generators, listener=listener)
