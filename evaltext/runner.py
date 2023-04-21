import logging
import os
from enum import Enum
from typing import List, Callable

from .base import ScoreListener
from .generator import (CohereGenerator, OpenAiChatGenerator, OpenAiGenerator,
                        TextGenerator)
from .recorder import ScoreRecorder


class Runner:
    prompts_dir: str
    output_dir: str
    listeners: List[ScoreListener]

    def __init__(self, generators: List[TextGenerator], listeners: List[ScoreRecorder]):
        self.generators = generators
        self.listeners = listeners

    def measure(self, path: str, scorer: Callable[[str], float]) -> List[float]:
        with open(path, "r") as f:
            prompt_name = os.path.basename(f.name)
            prompt = f.read()
            for gen in self.generators:
                logging.log(logging.INFO, f"measuring {path} - {gen.name}...")
                self._measure_with_generator(gen, prompt_name, prompt, scorer)

    def _measure_with_generator(self, generator: TextGenerator, scorer: Callable[[str], float], prompt_name: str,
                                prompt: str, max_retry_count: int = 1) -> bool:
        request_count = 0
        res = None
        while request_count < max_retry_count + 1:
            request_count += 1
            try:
                res = generator.generate(prompt)
            except Exception as e:
                logging.log(logging.ERROR, f"request failed: {e}")

        if res is None:
            return False

        score = scorer(res)
        for listener in self.listeners:
            listener.handle(prompt_name, generator.name, score)

        return True


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
    listener = ScoreRecorder(output_path)
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
    return Runner(generators=generators, listeners=[listener])
