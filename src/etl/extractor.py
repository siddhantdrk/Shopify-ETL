import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging
from ..models.order import Address, Customer, Order, LineItem

logger = logging.getLogger(__name__)

class ShopifyDataExtractor:
    """Extracts data from Shopify JSON files in a directory"""
    
    def __init__(self, data_directory: str):
        """
        Initialize the extractor
        
        Args:
            data_directory: Path to the directory containing Shopify JSON files
        """
        self.data_directory = Path(data_directory)
        if not self.data_directory.exists():
            raise ValueError(f"Directory {data_directory} does not exist")
        if not self.data_directory.is_dir():
            raise ValueError(f"{data_directory} is not a directory")

    def _get_json_files(self, file_pattern: str = "*.json") -> List[Path]:
        """
        Get all JSON files in the data directory
        
        Returns:
            List of Path objects for JSON files
        """
        return list(self.data_directory.glob(file_pattern))

    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Read and parse a JSON file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Parsed JSON data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise

    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        Parse datetime string from Shopify format
        
        Args:
            dt_str: Datetime string in Shopify format
            
        Returns:
            Parsed datetime object
        """
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except Exception as e:
            logger.error(f"Error parsing datetime {dt_str}: {str(e)}")
            raise

    def extract_order(self, order_data: Dict[str, Any]) -> Order:
        """
        Extract and validate a single order
        
        Args:
            order_data: Raw order data from JSON
            
        Returns:
            Validated Order object
        """
        try:
            # Convert datetime strings to datetime objects
            for dt_field in ['created_at', 'updated_at', 'processed_at']:
                if dt_field in order_data:
                    order_data[dt_field] = self._parse_datetime(order_data[dt_field])

            # Convert customer data
            if 'customer' in order_data:
                customer_data = order_data['customer']
                customer_data['created_at'] = self._parse_datetime(customer_data['created_at'])
                customer_data['updated_at'] = self._parse_datetime(customer_data['updated_at'])
                order_data['customer'] = Customer(**customer_data)

            # Convert addresses
            for addr_field in ['billing_address', 'shipping_address']:
                if addr_field in order_data:
                    order_data[addr_field] = Address(**order_data[addr_field])

            # Convert line items
            if 'line_items' in order_data:
                order_data['line_items'] = [
                    LineItem(**item) for item in order_data['line_items']
                ]

            return Order(**order_data)
        except Exception as e:
            logger.error(f"Error extracting order {order_data.get('id')}: {str(e)}")
            raise

    def extract_orders(self, file_pattern: str = "*.json") -> List[Order]:
        """
        Extract orders from all JSON files in the data directory
        
        Returns:
            List of extracted and validated Order objects
        """
        try:
            json_files = self._get_json_files(file_pattern)
            if not json_files:
                logger.warning(f"No JSON files found in {self.data_directory}")
                return []

            all_orders = []
            for file_path in json_files:
                try:
                    logger.info(f"Processing file: {file_path}")
                    data = self._read_json_file(file_path)
                    
                    if 'orders' not in data:
                        logger.warning(f"No 'orders' key found in {file_path}")
                        continue

                    for order_data in data['orders']:
                        try:
                            order = self.extract_order(order_data)
                            all_orders.append(order)
                        except Exception as e:
                            logger.error(f"Error processing order in {file_path}: {str(e)}")
                            continue

                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    continue

            logger.info(f"Successfully extracted {len(all_orders)} orders from {len(json_files)} files")
            return all_orders

        except Exception as e:
            logger.error(f"Error processing directory {self.data_directory}: {str(e)}")
            raise 