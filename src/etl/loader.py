from typing import List, Dict, Any
import logging
from ..database.clickhouse_client import ClickHouseClient

logger = logging.getLogger(__name__)

class ShopifyDataLoader:
    """Loads transformed Shopify data into ClickHouse"""

    def __init__(self, db_client: ClickHouseClient):
        """
        Initialize the loader
        
        Args:
            db_client: ClickHouse client instance
        """
        self.db_client = db_client

    def load_orders(self, orders: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """
        Load orders into the database
        
        Args:
            orders: List of transformed order data
            batch_size: Number of records to insert in each batch
        """
        try:
            self.db_client.insert_orders(orders, batch_size)
            logger.info(f"Successfully loaded {len(orders)} orders")
        except Exception as e:
            logger.error(f"Error loading orders: {str(e)}")
            raise

    def load_order_items(self, order_items: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """
        Load order items into the database
        
        Args:
            order_items: List of transformed order item data
            batch_size: Number of records to insert in each batch
        """
        try:
            self.db_client.insert_order_items(order_items, batch_size)
            logger.info(f"Successfully loaded {len(order_items)} order items")
        except Exception as e:
            logger.error(f"Error loading order items: {str(e)}")
            raise

    def load_data(self, orders: List[Dict[str, Any]], order_items: List[Dict[str, Any]], 
                 batch_size: int = 1000) -> None:
        """
        Load both orders and order items into the database
        
        Args:
            orders: List of transformed order data
            order_items: List of transformed order item data
            batch_size: Number of records to insert in each batch
        """
        try:
            # Load orders first
            self.load_orders(orders, batch_size)
            
            # Then load order items
            self.load_order_items(order_items, batch_size)
            
            logger.info("Successfully loaded all data")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise 