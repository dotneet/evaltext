import os
from typing import Any, Dict

import openai
import tiktoken

from . import TextGenerator


class OpenAiGenerator(TextGenerator):
    options: Dict[str, str]

    def __init__(self, options: Dict[str, str] = {}):
        initial_options = {
            'model': 'text-davinci-003',
            'apiKey': os.environ.get('OPENAI_API_KEY', ''),
            'temperature': 0,
        }
        self.options = {**initial_options, **options}  # type: ignore
        self.name = self.options.get('name') or 'openai-' + self.options['model']

    def generate(self, prompt: str) -> str:
        encoding = tiktoken.encoding_for_model(self.options['model'])
        prompt_tokens = encoding.encode(prompt)
        max_tokens = 4000 - len(prompt_tokens)
        response: Any = openai.Completion.create(
            model=self.options['model'],
            prompt=prompt,
            api_key=self.options['apiKey'],
            temperature=self.options['temperature'],
            max_tokens=max_tokens
        )

        return response['choices'][0]['text'] or ''
