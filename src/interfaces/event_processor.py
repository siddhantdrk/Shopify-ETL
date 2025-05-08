
from abc import ABC, abstractmethod
from typing import Dict, Any

class EventProcessor(ABC):
    @abstractmethod
    def process_event(self, event: Dict[str, Any]) -> None:
        pass
