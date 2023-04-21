from abc import ABC, abstractmethod


class TextGenerator(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
