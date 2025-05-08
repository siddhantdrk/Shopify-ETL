from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

class EventQueue(ABC):
    @abstractmethod
    def add_processor(self, processor: Callable[[Dict[str, Any]], None]) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def put(self, event: Dict[str, Any]) -> None:
        pass