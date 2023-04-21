import os
from typing import Any, Dict

import cohere

from . import TextGenerator


class CohereGenerator(TextGenerator):
    options:Dict[str,Any]
    client: cohere.Client

    def __init__(self, options: Dict[str,Any] = {}):
        initial_options = {
            'model': 'xlarge',
            'apiKey': os.environ.get('COHERE_API_KEY', ''),
            'temperature': 0,
        }
        self.options = {**initial_options, **(options or {})}
        self.client = cohere.Client(api_key=self.options['apiKey'])
        self.name = self.options.get('name') or 'cohere' + self.options['model']

    def generate(self, prompt: str) -> str:
        response = self.client.generate(
            prompt=prompt,
            model=self.options['model'],
            max_tokens=1000,
            temperature=self.options['temperature']
        )
        return response.generations[0].text
