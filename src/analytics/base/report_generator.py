from typing import Dict, Any
from datetime import datetime
from src.analytics.base.base_analytics import BaseAnalytics

class AnalyticsReportGenerator:
    """Generates HTML reports for base analytics metrics with formulas and explanations"""
    
    def __init__(self):
        self.analytics = BaseAnalytics()
        
    def _get_css_styles(self) -> str:
        """Returns CSS styles for the report"""
        return """
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .section {
                background: #fff;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .metric-card {
                background: #f8f9fa;
                border-left: 4px solid #007bff;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }
            .formula {
                background: #f1f8ff;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                margin: 10px 0;
            }
            .explanation {
                color: #666;
                font-size: 14px;
            }
            .chart-container {
                margin: 20px 0;
                height: 300px;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            .highlight {
                background-color: #fff3cd;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .insight {
                background: #e8f4f8;
                padding: 15px;
                border-radius: 4px;
                margin: 10px 0;
            }
        </style>
        """
    
    def _format_metric_value(self, value: Any, prefix: str = "", suffix: str = "") -> str:
        """Formats metric values with appropriate prefixes and suffixes"""
        if isinstance(value, (int, float)):
            if abs(value) >= 1000000:
                return f"{prefix}${value/1000000:.2f}M{suffix}"
            elif abs(value) >= 1000:
                return f"{prefix}${value/1000:.2f}K{suffix}"
            else:
                return f"{prefix}${value:.2f}{suffix}"
        return f"{prefix}{value}{suffix}"
    
    def _generate_sales_overview_section(self, metrics: Dict[str, Any]) -> str:
        """Generates HTML for sales overview section"""
        sales = metrics["sales_overview"]
        return f"""
        <div class="section">
            <h2>Sales Overview</h2>
            <div class="metric-card">
                <h3>Total Revenue</h3>
                <div class="metric-value">{self._format_metric_value(sales['total_revenue'])}</div>
                <div class="formula">Total Revenue = Σ(Order Total Price)</div>
                <div class="explanation">
                    The sum of all order values, representing the total income generated from sales.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Total Orders</h3>
                <div class="metric-value">{sales['total_orders']}</div>
                <div class="formula">Total Orders = Count(Orders)</div>
                <div class="explanation">
                    The total number of orders processed, indicating sales volume.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Average Order Value (AOV)</h3>
                <div class="metric-value">{self._format_metric_value(sales['average_order_value'])}</div>
                <div class="formula">AOV = Total Revenue ÷ Total Orders</div>
                <div class="explanation">
                    The average amount spent per order, a key metric for understanding customer spending patterns.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Total Customers</h3>
                <div class="metric-value">{sales['total_customers']}</div>
                <div class="formula">Total Customers = Count(Distinct Customer IDs)</div>
                <div class="explanation">
                    The number of unique customers who have made purchases.
                </div>
            </div>
        </div>
        """
    
    def _generate_customer_retention_section(self, metrics: Dict[str, Any]) -> str:
        """Generates HTML for customer retention section"""
        retention = metrics["customer_retention"]
        return f"""
        <div class="section">
            <h2>Customer Retention Metrics</h2>
            <div class="metric-card">
                <h3>Repeat Customer Rate</h3>
                <div class="metric-value">{retention['repeat_customer_rate']}%</div>
                <div class="formula">Repeat Customer Rate = (Customers with Multiple Orders ÷ Total Customers) × 100</div>
                <div class="explanation">
                    Percentage of customers who have made more than one purchase, indicating customer loyalty.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Average Orders per Customer</h3>
                <div class="metric-value">{retention['average_orders_per_customer']}</div>
                <div class="formula">Average Orders = Total Orders ÷ Total Customers</div>
                <div class="explanation">
                    The average number of orders placed by each customer, showing customer engagement level.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>90-Day Retention Rate</h3>
                <div class="metric-value">{retention['customer_retention_rate']}%</div>
                <div class="formula">90-Day Retention = (Customers Returning within 90 Days ÷ Total Customers) × 100</div>
                <div class="explanation">
                    Percentage of customers who make a repeat purchase within 90 days of their first order.
                </div>
            </div>
            
            <div class="insight">
                <h3>Key Insights</h3>
                <ul>
                    <li>A high repeat customer rate (>30%) indicates strong customer loyalty</li>
                    <li>Average orders per customer > 2 suggests successful customer retention strategies</li>
                    <li>90-day retention rate helps evaluate the effectiveness of post-purchase engagement</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_product_performance_section(self, metrics: Dict[str, Any]) -> str:
        """Generates HTML for product performance section"""
        products = metrics["product_performance"]["top_products"][:5]  # Top 5 products
        products_html = ""
        for product in products:
            products_html += f"""
            <div class="metric-card">
                <h3>{product['product_name']}</h3>
                <div class="metric-value">
                    Revenue: {self._format_metric_value(product['total_revenue'])}<br>
                    Quantity: {product['total_quantity']}<br>
                    Avg Price: {self._format_metric_value(product['average_price'])}
                </div>
                <div class="formula">
                    Revenue = Σ(Price × Quantity)<br>
                    Average Price = Total Revenue ÷ Total Quantity
                </div>
                <div class="explanation">
                    Performance metrics for this product, showing its contribution to overall sales.
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2>Top Product Performance</h2>
            {products_html}
            <div class="insight">
                <h3>Product Analysis</h3>
                <ul>
                    <li>Products with high revenue and quantity indicate strong demand</li>
                    <li>Average price helps identify pricing strategy effectiveness</li>
                    <li>Compare product performance to identify growth opportunities</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_discount_impact_section(self, metrics: Dict[str, Any]) -> str:
        """Generates HTML for discount impact section"""
        discounts = metrics["discount_impact"]
        return f"""
        <div class="section">
            <h2>Discount Impact Analysis</h2>
            <div class="metric-card">
                <h3>Discount Usage Rate</h3>
                <div class="metric-value">{discounts['discount_usage_rate']}%</div>
                <div class="formula">Discount Usage Rate = (Orders with Discounts ÷ Total Orders) × 100</div>
                <div class="explanation">
                    Percentage of orders that used discounts, indicating discount strategy effectiveness.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Average Discount Amount</h3>
                <div class="metric-value">{self._format_metric_value(discounts['average_discount_amount'])}</div>
                <div class="formula">Average Discount = Total Discount Amount ÷ Number of Discounted Orders</div>
                <div class="explanation">
                    The average discount value applied per order, showing discount generosity.
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Revenue Comparison</h3>
                <div class="metric-value">
                    With Discounts: {self._format_metric_value(discounts['revenue_with_discounts'])}<br>
                    Without Discounts: {self._format_metric_value(discounts['revenue_without_discounts'])}
                </div>
                <div class="formula">
                    Revenue with Discounts = Σ(Order Total Price where Discount > 0)<br>
                    Revenue without Discounts = Σ(Order Total Price where Discount = 0)
                </div>
                <div class="explanation">
                    Comparison of revenue from discounted vs. non-discounted orders.
                </div>
            </div>
            
            <div class="insight">
                <h3>Discount Strategy Insights</h3>
                <ul>
                    <li>High discount usage rate may indicate price sensitivity</li>
                    <li>Compare revenue with/without discounts to evaluate discount effectiveness</li>
                    <li>Monitor average discount amount to maintain profitability</li>
                </ul>
            </div>
        </div>
        """
    
    def generate_report(self) -> str:
        """Generates a complete HTML report with all metrics"""
        metrics = self.analytics.get_all_metrics()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shopify Analytics Report - {datetime.now().strftime('%Y-%m-%d')}</title>
            {self._get_css_styles()}
        </head>
        <body>
            <div class="container">
                <h1>Shopify Analytics Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                {self._generate_sales_overview_section(metrics)}
                {self._generate_customer_retention_section(metrics)}
                {self._generate_product_performance_section(metrics)}
                {self._generate_discount_impact_section(metrics)}
            </div>
        </body>
        </html>
        """
        
        return html
    
    def save_report(self, filepath: str) -> None:
        """Saves the HTML report to a file"""
        html = self.generate_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

def main():
    """Example usage of the report generator"""
    generator = AnalyticsReportGenerator()
    generator.save_report("analytics_report.html")
    print("Report generated successfully!")

if __name__ == "__main__":
    main() 