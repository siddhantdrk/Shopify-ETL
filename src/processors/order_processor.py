from src.etl.extractor import ShopifyDataExtractor
from src.etl.loader import ShopifyDataLoader
from src.etl.transformer import ShopifyDataTransformer
from src.interfaces.event_processor import EventProcessor
from typing import Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)

class OrderEventProcessor(EventProcessor):
    def __init__(self, extractor: ShopifyDataExtractor, transformer: ShopifyDataTransformer, loader: ShopifyDataLoader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def process_event(self, event: Dict[str, Any]) -> None:
        try:
            logger.info(f"Processing batch of orders")
            # Validate event structure
            if not isinstance(event, dict):
                raise ValueError(f"Expected dict, got {type(event)}")
            
            if 'orders' not in event:
                raise ValueError("No 'orders' key found in event")
            
            orders = event['orders']
            if not isinstance(orders, list):
                raise ValueError(f"Expected list of orders, got {type(orders)}")
            
            # Extract all orders
            extracted_orders = []
            extracted_items = []
            
            for order in orders:
                try:
                    if not isinstance(order, dict):
                        logger.error(f"Invalid order format")
                        continue
                        
                    if 'id' not in order:
                        logger.error(f"Order missing ID")
                        continue
                    
                    # Extract order
                    extracted_order = self.extractor.extract_order(order)
                    extracted_orders.append(extracted_order)
                    
                    # Extract items
                    items = self.transformer.transform_order_items(extracted_order)
                    extracted_items.extend(items)
                    
                except Exception as e:
                    logger.error(f"Error processing order {order.get('id', 'unknown')}: {str(e)}")
                    logger.error(f"Stack trace: {traceback.format_exc()}")
                    continue
            
            # Transform all orders at once
            transformed_orders = [self.transformer.transform_order(order) for order in extracted_orders]
            
            # Load all data at once
            if transformed_orders:
                logger.info(f"Loading {len(transformed_orders)} orders and {len(extracted_items)} items")
                self.loader.load_data(transformed_orders, extracted_items)
                logger.info(f"Successfully processed batch of {len(transformed_orders)} orders")
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")

    def _process_single_order(self, order: Dict[str, Any]) -> None:
        """Process a single order"""
        try:
            logger.info(f"Processing single order: {order.get('id', 'unknown')}")
            # Validate order structure
            if not isinstance(order, dict):
                raise ValueError(f"Expected order dict, got {type(order)}")
            
            # Get order ID safely
            order_id = order.get('id')
            if not order_id:
                raise ValueError("Order ID is missing")

            # Extract order
            logger.info(f"Extracting order {order_id}")
            extracted_order = self.extractor.extract_order(order)

            # Transform order
            logger.info(f"Transforming order {order_id}")
            transformed_order = self.transformer.transform_order(extracted_order)
            transformed_items = self.transformer.transform_order_items(extracted_order)
            
            # Load data
            logger.info(f"Loading order {order_id}")
            self.loader.load_data([transformed_order], transformed_items)
            logger.info(f"Successfully processed order: {order_id}")
            
        except Exception as e:
            logger.error(f"Error processing order {order.get('id', 'unknown')}: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            # Don't re-raise to keep the queue processing
