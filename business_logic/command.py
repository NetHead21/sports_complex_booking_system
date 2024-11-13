from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError("You must implement this method")
