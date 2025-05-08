import os
from typing import List, Dict, Any
from clickhouse_driver import Client
from dotenv import load_dotenv

load_dotenv()

class ClickHouseClient:
    def __init__(self):
        self.client = Client(
            host=os.getenv('CLICKHOUSE_HOST', '127.0.0.1'),
            port=int(os.getenv('CLICKHOUSE_PORT', 9000)),
            user=os.getenv('CLICKHOUSE_USER', 'default'),
            password=os.getenv('CLICKHOUSE_PASSWORD', ''),
            database=os.getenv('CLICKHOUSE_DATABASE', 'default')
        )
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Orders table
        self.client.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id UInt64,
                name String,
                email String,
                created_at DateTime,
                updated_at DateTime,
                processed_at DateTime,
                total_price Decimal(10,2),
                subtotal_price Decimal(10,2),
                total_tax Decimal(10,2),
                total_discounts Decimal(10,2),
                currency String,
                financial_status String,
                fulfillment_status String,
                customer_id UInt64,
                customer_email String,
                customer_first_name String,
                customer_last_name String,
                customer_phone String,
                billing_address_city String,
                billing_address_province String,
                billing_address_country String,
                shipping_address_city String,
                shipping_address_province String,
                shipping_address_country String,
                note String,
                tags String
            ) ENGINE = ReplacingMergeTree()
            ORDER BY (id, created_at)
            PRIMARY KEY id
        ''')

        # Order items table
        self.client.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id UInt64,
                order_id UInt64,
                name String,
                price Decimal(10,2),
                quantity UInt32,
                sku String,
                title String,
                variant_id UInt64,
                product_id UInt64,
                total_discount Decimal(10,2)
            ) ENGINE = ReplacingMergeTree()
            ORDER BY (id, order_id)
            PRIMARY KEY (id, order_id)
        ''')

    def insert_data(self, table_name: str, data: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """
        Generic method to insert data into any table with duplicate handling
        
        Args:
            table_name: Name of the table to insert into
            data: List of dictionaries containing the data to insert
            batch_size: Number of records to insert in each batch
        """
        if not data:
            return

        # Get column names from the first record
        columns = list(data[0].keys())
        
        # Prepare the insert query using ClickHouse's format
        query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES'
        
        # Process data in batches
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            values = [[record[col] for col in columns] for record in batch]
            
            try:
                self.client.execute(query, values)
            except Exception as e:
                print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
                raise
        
        # Force merge after insertion
        self.force_merge(table_name)

    def force_merge(self, table_name: str) -> None:
        """Force merge operation on the specified table"""
        try:
            self.client.execute(f'OPTIMIZE TABLE {table_name} FINAL')
        except Exception as e:
            print(f"Error during merge operation: {str(e)}")
            # Don't raise the error as merge is not critical

    def insert_orders(self, orders: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """Insert orders into the database with duplicate handling"""
        self.insert_data('orders', orders, batch_size)

    def insert_order_items(self, line_items: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """Insert line items into the database with duplicate handling"""
        self.insert_data('order_items', line_items, batch_size)

    def execute_query(self, query: str) -> Any:
        """Execute a custom query"""
        return self.client.execute(query) 