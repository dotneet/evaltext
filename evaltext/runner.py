from typing import List

from .generator import (CohereGenerator, OpenAiChatGenerator, OpenAiGenerator,
                        TextGenerator)


class Runner:
    def __init__(self, generators: List[TextGenerator]):
        self.generators = generators

    def run(self, prompt: str) -> List[str]:
        result: List[str] = []
        for gen in self.generators:
            res = gen.generate(prompt)
            result.append(res)

        return result


from enum import Enum


class GeneratorType(Enum):
    OPENAI_GPT4 = 'openai-gpt4'
    OPENAI_GPT_3_5_TURBO = 'openai-gpt-3.5-turbo'
    OPENAI_GPT_3_5_TURBO_0301 = 'openai-gpt-3.5-turbo-0301'
    OPENAI_DAVINCI_003 = 'openai-davinci-003'
    OPENAI_DAVINCI_002 = 'openai-davinci-002'
    COHERE_XLARGE = 'cohere-xlarge'
    COHERE_MEDIUM = 'cohere-medium'
    OPENAI_BABBAGE_001 = 'openai-babbage-001'


def create_runner(types: List[GeneratorType]) -> Runner:
    generators: List[TextGenerator] = []
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
    return Runner(generators=generators)
