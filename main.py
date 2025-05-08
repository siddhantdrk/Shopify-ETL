import logging
from typing import Optional
from pathlib import Path
import time

from src.etl.extractor import ShopifyDataExtractor
from src.etl.transformer import ShopifyDataTransformer
from src.etl.loader import ShopifyDataLoader
from src.database.clickhouse_client import ClickHouseClient
from src.services.file_watcher import FileWatcherService
from src.services.event_queue import InMemoryEventQueue
from src.etl.pipeline import ETLPipeline

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the ETL pipeline"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize components
    data_dir = Path("data")
    db_client = ClickHouseClient()
    
    # Create dependencies
    file_watcher = FileWatcherService(str(data_dir))
    event_queue = InMemoryEventQueue()
    extractor = ShopifyDataExtractor(str(data_dir))
    transformer = ShopifyDataTransformer()
    loader = ShopifyDataLoader(db_client)
    
    try:
        # Create and run pipeline
        pipeline = ETLPipeline(
            data_dir=str(data_dir),
            file_watcher=file_watcher,
            event_queue=event_queue,
            extractor=extractor,
            transformer=transformer,
            loader=loader
        )
        
        # Run initial ETL
        pipeline.run()
        
        # Keep running to process new orders
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pipeline.stop()
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()