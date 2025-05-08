from typing import Dict, Any, Sequence
from src.database.clickhouse_client import ClickHouseClient

class BaseAnalytics:
    """
    A class to perform basic yet impactful analytics on Shopify order data using ClickHouse.
    This module focuses on fundamental metrics that are easy to understand
    and can drive immediate business decisions.
    """
    
    def __init__(self):
        """Initialize the BaseAnalytics with ClickHouse connection"""
        self.client = ClickHouseClient()
        
    def get_sales_overview(self) -> Dict[str, Any]:
        """
        Get a high-level overview of sales metrics.
        
        Returns:
            Dict containing:
            - total_revenue: Total revenue from all orders
            - total_orders: Total number of orders
            - average_order_value: Average revenue per order
            - total_customers: Number of unique customers
        """
        query = """
        SELECT 
            sum(total_price) as total_revenue,
            count() as total_orders,
            sum(total_price) / count() as average_order_value,
            count(DISTINCT customer_id) as total_customers
        FROM orders
        """
        result = self.client.execute_query(query)
        if not result or not result[0]:
            return {
                "total_revenue": 0.0,
                "total_orders": 0,
                "average_order_value": 0.0,
                "total_customers": 0
            }
            
        data = {
            "total_revenue": result[0][0],
            "total_orders": result[0][1],
            "average_order_value": result[0][2],
            "total_customers": result[0][3]
        }
        
        return {
            "total_revenue": round(float(data["total_revenue"]), 2),
            "total_orders": data["total_orders"],
            "average_order_value": round(float(data["average_order_value"]), 2),
            "total_customers": data["total_customers"]
        }
    
    def get_monthly_sales_trend(self) -> Dict[str, Sequence[Dict[str, Any]]]:
        """
        Get monthly sales trends to identify seasonal patterns.
        
        Returns:
            Dict containing monthly data with:
            - month: Month and year
            - revenue: Total revenue for the month
            - orders: Number of orders in the month
            - customers: Number of unique customers in the month
        """
        query = """
        SELECT 
            toYYYYMM(created_at) as month,
            sum(total_price) as revenue,
            count() as orders,
            count(DISTINCT customer_id) as customers
        FROM orders
        GROUP BY month
        ORDER BY month
        """
        result = self.client.execute_query(query)
        if not result:
            return {"monthly_trend": []}
            
        data = [
            {
                "month": str(row[0]),
                "revenue": round(float(row[1]), 2),
                "orders": row[2],
                "customers": row[3]
            }
            for row in result
        ]
        
        return {"monthly_trend": data}
    
    def get_customer_retention_metrics(self) -> Dict[str, Any]:
        """
        Calculate basic customer retention metrics.
        
        Returns:
            Dict containing:
            - repeat_customer_rate: Percentage of customers who made multiple orders
            - average_orders_per_customer: Average number of orders per customer
            - customer_retention_rate: Percentage of customers who returned within 90 days
        """
        # Get repeat customer rate and average orders
        query = """
        WITH customer_orders AS (
            SELECT 
                customer_id,
                count() as order_count
            FROM orders
            GROUP BY customer_id
        )
        SELECT 
            countIf(order_count > 1) * 100.0 / count() as repeat_customer_rate,
            avg(order_count) as average_orders_per_customer
        FROM customer_orders
        """
        result = self.client.execute_query(query)
        if not result or not result[0]:
            return {
                "repeat_customer_rate": 0.0,
                "average_orders_per_customer": 0.0,
                "customer_retention_rate": 0.0
            }
            
        data = {
            "repeat_customer_rate": result[0][0],
            "average_orders_per_customer": result[0][1]
        }
        
        # Get 90-day retention rate
        retention_query = """
        WITH customer_first_orders AS (
            SELECT 
                customer_id,
                min(created_at) as first_order_date
            FROM orders
            GROUP BY customer_id
        ),
        customer_second_orders AS (
            SELECT 
                o.customer_id,
                min(o.created_at) as second_order_date
            FROM orders o
            JOIN customer_first_orders f ON o.customer_id = f.customer_id
            WHERE o.created_at > f.first_order_date
            GROUP BY o.customer_id
        )
        SELECT 
            countIf(dateDiff('day', first_order_date, second_order_date) <= 90) * 100.0 / count() as retention_rate
        FROM customer_first_orders f
        LEFT JOIN customer_second_orders s ON f.customer_id = s.customer_id
        """
        retention_result = self.client.execute_query(retention_query)
        retention_rate = retention_result[0][0] if retention_result and retention_result[0] else 0
        
        return {
            "repeat_customer_rate": round(float(data["repeat_customer_rate"]), 2),
            "average_orders_per_customer": round(float(data["average_orders_per_customer"]), 2),
            "customer_retention_rate": round(float(retention_rate), 2)
        }
    
    def get_product_performance(self) -> Dict[str, Sequence[Dict[str, Any]]]:
        """
        Get basic product performance metrics.
        
        Returns:
            Dict containing top products with:
            - product_name: Name of the product
            - total_quantity: Total quantity sold
            - total_revenue: Total revenue from the product
            - average_price: Average price per unit
        """
        query = """
        SELECT 
            name as product_name,
            sum(quantity) as total_quantity,
            sum(price * quantity) as total_revenue,
            sum(price * quantity) / sum(quantity) as average_price
        FROM order_items
        GROUP BY product_name
        ORDER BY total_revenue DESC
        LIMIT 10
        """
        result = self.client.execute_query(query)
        if not result:
            return {"top_products": []}
            
        data = [
            {
                "product_name": row[0],
                "total_quantity": row[1],
                "total_revenue": round(float(row[2]), 2),
                "average_price": round(float(row[3]), 2)
            }
            for row in result
        ]
        
        return {"top_products": data}
    
    def get_discount_impact(self) -> Dict[str, Any]:
        """
        Analyze the impact of discounts on sales.
        
        Returns:
            Dict containing:
            - discount_usage_rate: Percentage of orders using discounts
            - average_discount_amount: Average discount amount per order
            - total_discount_amount: Total discount amount given
            - revenue_with_discounts: Revenue from orders with discounts
            - revenue_without_discounts: Revenue from orders without discounts
        """
        query = """
        SELECT 
            countIf(total_discounts > 0) * 100.0 / count() as discount_usage_rate,
            sumIf(total_discounts, total_discounts > 0) / countIf(total_discounts > 0) as average_discount_amount,
            sum(total_discounts) as total_discount_amount,
            sumIf(total_price, total_discounts > 0) as revenue_with_discounts,
            sumIf(total_price, total_discounts = 0) as revenue_without_discounts
        FROM orders
        """
        result = self.client.execute_query(query)
        if not result or not result[0]:
            return {
                "discount_usage_rate": 0.0,
                "average_discount_amount": 0.0,
                "total_discount_amount": 0.0,
                "revenue_with_discounts": 0.0,
                "revenue_without_discounts": 0.0
            }
            
        data = {
            "discount_usage_rate": result[0][0],
            "average_discount_amount": result[0][1],
            "total_discount_amount": result[0][2],
            "revenue_with_discounts": result[0][3],
            "revenue_without_discounts": result[0][4]
        }
        
        return {
            "discount_usage_rate": round(float(data["discount_usage_rate"]), 2),
            "average_discount_amount": round(float(data["average_discount_amount"]), 2),
            "total_discount_amount": round(float(data["total_discount_amount"]), 2),
            "revenue_with_discounts": round(float(data["revenue_with_discounts"]), 2),
            "revenue_without_discounts": round(float(data["revenue_without_discounts"]), 2)
        }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all basic analytics metrics in one call.
        
        Returns:
            Dict containing all metrics from other methods
        """
        return {
            "sales_overview": self.get_sales_overview(),
            "monthly_trends": self.get_monthly_sales_trend(),
            "customer_retention": self.get_customer_retention_metrics(),
            "product_performance": self.get_product_performance(),
            "discount_impact": self.get_discount_impact()
        }

def main():
    """Example usage of the BaseAnalytics class"""
    # Initialize analytics
    analytics = BaseAnalytics()
    
    # Get all metrics
    metrics = analytics.get_all_metrics()
    
    # Print results in a readable format
    print("\n=== Sales Overview ===")
    for key, value in metrics["sales_overview"].items():
        print(f"{key}: {value}")
    
    print("\n=== Customer Retention ===")
    for key, value in metrics["customer_retention"].items():
        print(f"{key}: {value}%")
    
    print("\n=== Discount Impact ===")
    for key, value in metrics["discount_impact"].items():
        print(f"{key}: ${value}")
    
    print("\n=== Top 5 Products ===")
    for product in metrics["product_performance"]["top_products"][:5]:
        print(f"\nProduct: {product['product_name']}")
        print(f"Quantity Sold: {product['total_quantity']}")
        print(f"Total Revenue: ${product['total_revenue']}")
        print(f"Average Price: ${product['average_price']}")

if __name__ == "__main__":
    main() 