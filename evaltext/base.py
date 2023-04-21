from abc import ABC, abstractmethod


class ScoreListener(ABC):
    @abstractmethod
    def handle(self, prompt_name: str, model_name: str, score: float) -> None:
        pass
