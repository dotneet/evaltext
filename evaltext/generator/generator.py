from abc import ABC, abstractmethod

class TextGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
