import logging
from typing import Optional
from pathlib import Path

from src.etl.extractor import ShopifyDataExtractor
from src.etl.transformer import ShopifyDataTransformer
from src.etl.loader import ShopifyDataLoader
from src.database.clickhouse_client import ClickHouseClient
from src.utils.data_generator import ShopifyOrderGenerator

logger = logging.getLogger(__name__)

class ETLPipeline:
    """Main ETL pipeline for processing Shopify data"""

    def __init__(self, data_dir: str, db_client: Optional[ClickHouseClient] = None):
        """
        Initialize the ETL pipeline
        
        Args:
            data_dir: Directory containing Shopify JSON files
            db_client: Optional ClickHouse client instance
        """
        self.extractor = ShopifyDataExtractor(data_dir)
        self.transformer = ShopifyDataTransformer()
        self.loader = ShopifyDataLoader(db_client or ClickHouseClient())

    def run(self, file_pattern: str = "*.json", batch_size: int = 1000) -> None:
        """
        Run the complete ETL pipeline
        
        Args:
            file_pattern: Pattern to match JSON files
            batch_size: Number of records to insert in each batch
        """
        try:
            # Extract
            logger.info("Starting data extraction...")
            orders = self.extractor.extract_orders(file_pattern)
            if not orders:
                logger.warning("No orders found to process")
                return

            # Transform
            logger.info("Starting data transformation...")
            transformed_orders, transformed_line_items = self.transformer.transform_orders(orders)

            # Load
            logger.info("Starting data loading...")
            self.loader.load_data(transformed_orders, transformed_line_items, batch_size)

            logger.info("ETL pipeline completed successfully")
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            raise

def main():
    """Main entry point for the ETL pipeline"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get data directory from environment or use default
    data_dir = Path("data")
    
    try:
        # Initialize and run pipeline
        pipeline = ETLPipeline(str(data_dir))
        pipeline.run()
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()