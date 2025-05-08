from typing import Any, Dict
from src.etl.extractor import ShopifyDataExtractor
from src.etl.loader import ShopifyDataLoader
from src.etl.transformer import ShopifyDataTransformer
from src.interfaces.file_watcher import FileWatcher
from src.interfaces.event_queue import EventQueue
from src.processors.order_processor import OrderEventProcessor
import logging

logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(
        self,
        data_dir: str,
        file_watcher: FileWatcher,
        event_queue: EventQueue,
        extractor: ShopifyDataExtractor,
        transformer: ShopifyDataTransformer,
        loader: ShopifyDataLoader
    ):
        self.file_watcher = file_watcher
        self.event_queue = event_queue
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.order_processor = OrderEventProcessor(extractor, transformer, loader)
        self._setup_event_processing()

    def _setup_event_processing(self):
        self.event_queue.add_processor(self.order_processor.process_event)
        self.event_queue.start()
        self.file_watcher.start(self._on_new_order)

    def _on_new_order(self, order_data: Dict[str, Any]):
        try:
            self.event_queue.put(order_data)
            logger.info(f"Queued new order: {order_data.get('id')}")
        except Exception as e:
            logger.error(f"Error queuing order: {str(e)}")

    def run(self, file_pattern: str = "*.json", batch_size: int = 1000) -> None:
        try:
            # Process existing files
            logger.info("Starting data extraction...")
            orders = self.extractor.extract_orders(file_pattern)
            if not orders:
                logger.warning("No orders found to process")
                return

            # Transform and load existing orders
            transformed_orders, transformed_line_items = self.transformer.transform_orders(orders)
            self.loader.load_data(transformed_orders, transformed_line_items, batch_size)

            logger.info("ETL pipeline completed successfully")
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            raise

    def stop(self):
        self.event_queue.stop()
        self.file_watcher.stop()
        logger.info("ETL pipeline stopped")
