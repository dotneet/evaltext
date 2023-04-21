from abc import ABC, abstractmethod


class ScoreListener(ABC):
    @abstractmethod
    def handle(self, prompt: str, prompt_name: str, model_name: str, response: str, elapsed: float,
               score: float) -> None:
        pass
