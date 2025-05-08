from queue import Queue, Empty, Full
from threading import Thread
import logging
from typing import Dict, Any, Callable, List
from src.interfaces.event_queue import EventQueue

logger = logging.getLogger(__name__)

class InMemoryEventQueue(EventQueue):
    def __init__(self, max_size: int = 1000):
        self.queue = Queue(maxsize=max_size)
        self.processors: List[Callable[[Dict[str, Any]], None]] = []
        self.running = False
        self.worker_thread = None

    def add_processor(self, processor: Callable[[Dict[str, Any]], None]):
        self.processors.append(processor)

    def start(self):
        self.running = True
        self.worker_thread = Thread(target=self._process_events)
        self.worker_thread.start()
        logger.info("Event queue started")

    def stop(self):
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
        logger.info("Event queue stopped")

    def put(self, event: Dict[str, Any]):
        try:
            self.queue.put(event, block=False)
            logger.debug(f"Added event to queue: {event.get('id')}")
        except Full:
            logger.warning("Event queue is full, dropping event")

    def _process_events(self):
        while self.running:
            try:
                event = self.queue.get(timeout=1)
                for processor in self.processors:
                    try:
                        processor(event)
                    except Exception as e:
                        logger.error(f"Error processing event: {str(e)}")
                self.queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Unexpected error in event processing: {str(e)}")
                continue
