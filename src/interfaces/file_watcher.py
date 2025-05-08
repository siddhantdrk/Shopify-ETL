from abc import ABC, abstractmethod
from typing import Callable

class FileWatcher(ABC):
    @abstractmethod
    def start(self, callback: Callable) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass