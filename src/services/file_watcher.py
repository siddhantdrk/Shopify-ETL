import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from src.interfaces.file_watcher import FileWatcher
import logging
import traceback
from typing import Callable, Dict, Any, Set
from pathlib import Path
import time

logger = logging.getLogger(__name__)

class ShopifyFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Dict[str, Any]], None]):
        self.callback = callback
        self.processed_files: Set[str] = set()

    def _process_file(self, file_path: str):
        if file_path in self.processed_files:
            return

        # Wait for file to be fully written
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                if not Path(file_path).exists():
                    time.sleep(retry_delay)
                    continue
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        time.sleep(retry_delay)
                        continue
                        
                    data = json.loads(content)
                    if not isinstance(data, dict):
                        raise ValueError(f"Expected dict, got {type(data)}")
                    
                    if 'orders' not in data:
                        logger.warning(f"No 'orders' key found in {file_path}")
                        return
                    
                    if not isinstance(data['orders'], list):
                        raise ValueError(f"Expected list of orders, got {type(data['orders'])}")
                    
                    # Process all orders at once
                    logger.info(f"Processing {len(data['orders'])} orders from {file_path}")
                    self.callback(data)  # Pass the entire data object
                    
                self.processed_files.add(file_path)
                logger.info(f"Successfully processed file: {file_path}")
                break
                    
            except json.JSONDecodeError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise

    def on_created(self, event: FileCreatedEvent):
        if event.is_directory:
            return
        if not event.src_path.endswith('.json'):
            return
        logger.info(f"New file detected: {event.src_path}")
        self._process_file(event.src_path)

class FileWatcherService(FileWatcher):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.observer = Observer()
        self.handler = None

    def start(self, callback: Callable):
        self.handler = ShopifyFileHandler(callback)
        self.observer.schedule(self.handler, str(self.data_dir), recursive=False)
        self.observer.start()
        logger.info(f"Started watching directory: {self.data_dir}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        logger.info("Stopped watching directory")
