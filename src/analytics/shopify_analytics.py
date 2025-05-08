import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class ShopifyAnalytics:
    def __init__(self, clickhouse_client):
        """Initialize analytics with ClickHouse client"""
        self.client = clickhouse_client

    def _execute_query(self, query: str) -> pd.DataFrame:
        """Execute query and return results as DataFrame"""
        try:
            result = self.client.execute_query(query)
            # Get column names from the query
            column_names = [col.split(' as ')[-1].strip() for col in query.split('SELECT')[1].split('FROM')[0].split(',')]
            column_names = [col.split()[-1] for col in column_names]  # Handle cases with 'as'
            return pd.DataFrame(result, columns=column_names)
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise

    def get_sales_over_time(self, days: int = 30) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze sales trends over time"""
        query = f"""
        SELECT 
            toDate(created_at) as date,
            count() as order_count,
            sum(total_price) as total_sales,
            avg(total_price) as average_order_value
        FROM orders
        WHERE created_at >= now() - INTERVAL {days} DAY
        GROUP BY date
        ORDER BY date
        """
        
        df = self._execute_query(query)
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
        
        # Create visualization
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['total_sales'], name="Total Sales"),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['order_count'], name="Order Count"),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Sales and Order Trends Over Time",
            xaxis_title="Date",
            hovermode="x unified"
        )
        
        fig.update_yaxes(title_text="Total Sales ($)", secondary_y=False)
        fig.update_yaxes(title_text="Order Count", secondary_y=True)
        
        return df, fig

    def get_product_performance(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze product performance metrics"""
        query = """
        SELECT 
            title as product_name,
            count() as units_sold,
            sum(quantity) as total_quantity,
            sum(price * quantity) as total_revenue,
            avg(price) as average_price
        FROM order_items
        GROUP BY product_name
        ORDER BY total_revenue DESC
        LIMIT 10
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.bar(
            df,
            x='product_name',
            y='total_revenue',
            title="Top 10 Products by Revenue",
            labels={'total_revenue': 'Total Revenue ($)', 'product_name': 'Product'},
            color='units_sold',
            color_continuous_scale='Viridis'
        )
        
        return df, fig

    def get_customer_segments(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze customer segments and their behavior"""
        query = """
        SELECT 
            customer_id,
            count() as order_count,
            sum(total_price) as total_spent,
            avg(total_price) as average_order_value,
            min(created_at) as first_order,
            max(created_at) as last_order
        FROM orders
        GROUP BY customer_id
        """
        
        df = self._execute_query(query)
        
        # Calculate RFM metrics
        df['last_order'] = pd.to_datetime(df['last_order'])
        df['recency'] = df['last_order'].apply(lambda x: (pd.Timestamp.now() - x).days)
        df['frequency'] = df['order_count']
        df['monetary'] = df['total_spent']
        
        # Create visualization
        fig = px.scatter_3d(
            df,
            x='recency',
            y='frequency',
            z='monetary',
            title="Customer Segments (RFM Analysis)",
            labels={
                'recency': 'Recency (days)',
                'frequency': 'Frequency (orders)',
                'monetary': 'Monetary Value ($)'
            }
        )
        
        return df, fig

    def get_payment_analytics(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze payment and financial metrics"""
        query = """
        SELECT 
            financial_status,
            count() as order_count,
            sum(total_price) as total_revenue,
            sum(total_discounts) as total_discounts,
            sum(total_tax) as total_tax
        FROM orders
        GROUP BY financial_status
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
        
        fig.add_trace(
            go.Pie(
                labels=df['financial_status'],
                values=df['order_count'],
                name="Order Distribution"
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=df['financial_status'],
                y=df['total_revenue'],
                name="Revenue by Status"
            ),
            row=1, col=2
        )
        
        fig.update_layout(title_text="Payment Status Analysis")
        
        return df, fig

    def get_geographic_analysis(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze sales by geographic location"""
        query = """
        SELECT 
            shipping_address_country as country,
            count() as order_count,
            sum(total_price) as total_revenue
        FROM orders
        GROUP BY country
        ORDER BY total_revenue DESC
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.choropleth(
            df,
            locations='country',
            locationmode='country names',
            color='total_revenue',
            hover_name='country',
            color_continuous_scale='Viridis',
            title="Sales by Country"
        )
        
        return df, fig

    def get_time_based_metrics(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze time-based metrics"""
        query = """
        SELECT 
            toHour(created_at) as hour,
            toDayOfWeek(created_at) as day_of_week,
            count() as order_count,
            sum(total_price) as total_revenue
        FROM orders
        GROUP BY hour, day_of_week
        ORDER BY day_of_week, hour
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.density_heatmap(
            df,
            x='hour',
            y='day_of_week',
            z='order_count',
            title="Order Activity Heatmap",
            labels={
                'hour': 'Hour of Day',
                'day_of_week': 'Day of Week',
                'order_count': 'Number of Orders'
            }
        )
        
        return df, fig

    def get_discount_analysis(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze discount usage and impact"""
        query = '''
        SELECT 
            count() as order_count,
            sum(total_discounts) as total_discount_amount,
            avg(total_discounts) as average_discount
        FROM orders
        WHERE total_discounts > 0
        '''
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.bar(
            x=['Orders with Discounts'],
            y=[df['order_count'].iloc[0]],
            title='Number of Orders with Discounts',
            labels={'x': '', 'y': 'Number of Orders'}
        )
        
        # Log summary statistics
        logger.info(f"Discount Analysis:")
        logger.info(f"Total orders with discounts: {df['order_count'].iloc[0]}")
        logger.info(f"Total discount amount: ${df['total_discount_amount'].iloc[0]:.2f}")
        logger.info(f"Average discount per order: ${df['average_discount'].iloc[0]:.2f}")
        
        return df, fig

    def get_product_category_analysis(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze product categories and their performance"""
        query = """
        SELECT 
            title as product_name,
            count() as order_count,
            sum(quantity) as total_quantity,
            sum(price * quantity) as total_revenue,
            avg(price) as average_price
        FROM order_items
        GROUP BY product_name
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.treemap(
            df,
            path=['product_name'],
            values='total_revenue',
            color='order_count',
            title="Product Category Performance",
            color_continuous_scale='Viridis'
        )
        
        return df, fig

    def get_customer_lifetime_value(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Calculate and analyze customer lifetime value"""
        query = """
        SELECT 
            customer_id,
            count() as order_count,
            sum(total_price) as total_spent,
            min(created_at) as first_order,
            max(created_at) as last_order
        FROM orders
        GROUP BY customer_id
        """
        
        df = self._execute_query(query)
        
        # Calculate CLV
        df['customer_age'] = (pd.to_datetime(df['last_order']) - pd.to_datetime(df['first_order'])).dt.days
        # Convert decimal to float before calculation
        df['total_spent'] = df['total_spent'].astype(float)
        df['clv'] = df['total_spent'] / (df['customer_age'] / 365.0)  # Annual CLV
        
        # Create visualization
        fig = px.histogram(
            df,
            x='clv',
            nbins=50,
            title="Customer Lifetime Value Distribution",
            labels={'clv': 'Annual CLV ($)'}
        )
        
        return df, fig

    def get_inventory_turnover(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze inventory turnover rates"""
        query = """
        SELECT 
            title as product_name,
            sum(quantity) as total_quantity,
            count() as order_count,
            sum(price * quantity) as total_revenue
        FROM order_items
        GROUP BY product_name
        """
        
        df = self._execute_query(query)
        
        # Convert total_revenue to float
        df['total_revenue'] = df['total_revenue'].astype(float)
        
        # Calculate turnover rate
        df['turnover_rate'] = df['total_quantity'] / df['order_count']
        
        # Create visualization
        fig = px.scatter(
            df,
            x='total_quantity',
            y='turnover_rate',
            size='total_revenue',
            color='order_count',
            hover_name='product_name',
            title="Inventory Turnover Analysis",
            labels={
                'total_quantity': 'Total Quantity Sold',
                'turnover_rate': 'Turnover Rate',
                'total_revenue': 'Total Revenue',
                'order_count': 'Number of Orders'
            }
        )
        
        return df, fig

    def get_seasonal_trends(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze seasonal trends in sales"""
        query = """
        SELECT 
            toMonth(created_at) as month,
            toYear(created_at) as year,
            count() as order_count,
            sum(total_price) as total_revenue
        FROM orders
        GROUP BY year, month
        ORDER BY year, month
        """
        
        df = self._execute_query(query)
        
        # Create visualization
        fig = px.line(
            df,
            x='month',
            y='total_revenue',
            color='year',
            title="Seasonal Sales Trends",
            labels={
                'month': 'Month',
                'total_revenue': 'Total Revenue ($)',
                'year': 'Year'
            }
        )
        
        return df, fig

    def get_order_aging_analysis(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Simple analysis of orders by their status"""
        query = """
        SELECT 
            financial_status,
            fulfillment_status,
            count() as order_count,
            avg(dateDiff('hour', created_at, updated_at)) as avg_order_time
        FROM orders
        WHERE created_at >= now() - INTERVAL 90 DAY
        GROUP BY financial_status, fulfillment_status
        ORDER BY order_count DESC
        """
        
        try:
            # Execute query and get results
            result = self.client.execute_query(query)
            
            # Create DataFrame with explicit column names
            df = pd.DataFrame(result, columns=[
                'financial_status', 'fulfillment_status', 'order_count', 'avg_order_time'
            ])
            
            # Debug logging to check column names
            logger.info(f"Order Status Analysis DataFrame columns: {df.columns.tolist()}")
            
            # Create a simple visualization with proper subplot types for pie charts
            fig = make_subplots(
                rows=1, cols=2,
                specs=[[{"type": "pie"}, {"type": "pie"}]],
                subplot_titles=(
                    "Orders by Financial Status",
                    "Orders by Fulfillment Status"
                )
            )
            
            # Financial Status Pie Chart
            financial_status_counts = df.groupby('financial_status')['order_count'].sum()
            fig.add_trace(
                go.Pie(
                    labels=financial_status_counts.index,
                    values=financial_status_counts.values,
                    name="Financial Status",
                    textinfo='label+value+percent'
                ),
                row=1, col=1
            )
            
            # Fulfillment Status Pie Chart
            fulfillment_status_counts = df.groupby('fulfillment_status')['order_count'].sum()
            fig.add_trace(
                go.Pie(
                    labels=fulfillment_status_counts.index,
                    values=fulfillment_status_counts.values,
                    name="Fulfillment Status",
                    textinfo='label+value+percent'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text="Order Status Distribution",
                height=600,
                showlegend=True
            )
            
            # Log simple insights
            logger.info("\nOrder Status Analysis:")
            logger.info(f"Total orders analyzed: {df['order_count'].sum()}")
            
            logger.info("\nFinancial Status Distribution:")
            for status, count in financial_status_counts.items():
                logger.info(f"- {status}: {count} orders")
            
            logger.info("\nFulfillment Status Distribution:")
            for status, count in fulfillment_status_counts.items():
                logger.info(f"- {status}: {count} orders")
            
            return df, fig
            
        except Exception as e:
            logger.error(f"Error in order status analysis: {str(e)}")
            logger.error(f"DataFrame columns: {df.columns.tolist() if 'df' in locals() else 'No DataFrame'}")
            raise

    def get_order_aging_trends(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze order aging trends over time"""
        query = """
        WITH daily_aging AS (
            SELECT 
                toDate(created_at) as date,
                financial_status,
                fulfillment_status,
                dateDiff('hour', created_at, processed_at) as processing_time,
                dateDiff('hour', processed_at, updated_at) as fulfillment_time,
                dateDiff('hour', created_at, updated_at) as total_order_age
            FROM orders
            WHERE created_at >= now() - INTERVAL 90 DAY
        )
        SELECT 
            date,
            financial_status,
            fulfillment_status,
            count() as order_count,
            avg(processing_time) as processing_time_avg,
            avg(fulfillment_time) as fulfillment_time_avg,
            avg(total_order_age) as total_age_avg
        FROM daily_aging
        GROUP BY date, financial_status, fulfillment_status
        ORDER BY date, financial_status, fulfillment_status
        """
        
        try:
            # Execute query and get results
            result = self.client.execute_query(query)
            
            # Create DataFrame with explicit column names
            df = pd.DataFrame(result, columns=[
                'date', 'financial_status', 'fulfillment_status', 'order_count',
                'processing_time_avg', 'fulfillment_time_avg', 'total_age_avg'
            ])
            
            # Debug logging to check column names
            logger.info(f"Order Aging Trends DataFrame columns: {df.columns.tolist()}")
            
            # Create visualization
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=(
                    "Processing Time Trends",
                    "Fulfillment Time Trends",
                    "Total Order Age Trends"
                )
            )
            
            # Plot processing time trends
            for status in df['financial_status'].unique():
                status_data = df[df['financial_status'] == status]
                fig.add_trace(
                    go.Scatter(
                        x=status_data['date'],
                        y=status_data['processing_time_avg'],
                        name=f"Processing - {status}",
                        mode='lines+markers'
                    ),
                    row=1, col=1
                )
            
            # Plot fulfillment time trends
            for status in df['fulfillment_status'].unique():
                status_data = df[df['fulfillment_status'] == status]
                fig.add_trace(
                    go.Scatter(
                        x=status_data['date'],
                        y=status_data['fulfillment_time_avg'],
                        name=f"Fulfillment - {status}",
                        mode='lines+markers'
                    ),
                    row=2, col=1
                )
            
            # Plot total order age trends
            for status in df['financial_status'].unique():
                status_data = df[df['financial_status'] == status]
                fig.add_trace(
                    go.Scatter(
                        x=status_data['date'],
                        y=status_data['total_age_avg'],
                        name=f"Total Age - {status}",
                        mode='lines+markers'
                    ),
                    row=3, col=1
                )
            
            fig.update_layout(
                title_text="Order Aging Trends Over Time",
                height=1200,
                showlegend=True
            )
            
            # Update y-axis labels
            fig.update_yaxes(title_text="Hours", row=1, col=1)
            fig.update_yaxes(title_text="Hours", row=2, col=1)
            fig.update_yaxes(title_text="Hours", row=3, col=1)
            
            # Log summary statistics
            logger.info("Order Aging Trends Summary:")
            logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
            logger.info(f"Total orders analyzed: {df['order_count'].sum()}")
            logger.info(f"Average processing time: {df['processing_time_avg'].mean():.2f} hours")
            logger.info(f"Average fulfillment time: {df['fulfillment_time_avg'].mean():.2f} hours")
            logger.info(f"Average total order age: {df['total_age_avg'].mean():.2f} hours")
            
            return df, fig
            
        except Exception as e:
            logger.error(f"Error in order aging trends: {str(e)}")
            logger.error(f"DataFrame columns: {df.columns.tolist() if 'df' in locals() else 'No DataFrame'}")
            raise

    def get_business_performance_metrics(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze key business performance metrics and KPIs"""
        query = """
        WITH order_metrics AS (
            SELECT 
                toDate(created_at) as date,
                -- Revenue metrics
                total_price as order_value,
                total_discounts as discount_amount,
                total_tax as tax_amount,
                -- Time metrics
                dateDiff('hour', created_at, processed_at) as processing_time,
                dateDiff('hour', processed_at, updated_at) as fulfillment_time,
                -- Status metrics
                financial_status,
                fulfillment_status,
                -- Customer metrics
                customer_id
            FROM orders
            WHERE created_at >= now() - INTERVAL 90 DAY
        )
        SELECT 
            date,
            -- Revenue KPIs
            sum(order_value) as daily_revenue,
            sum(discount_amount) as total_discounts,
            avg(order_value) as average_order_value,
            sum(discount_amount) / sum(order_value) * 100 as discount_rate,
            -- Conversion metrics
            count(DISTINCT customer_id) as unique_customers,
            count() as total_orders,
            count() / count(DISTINCT customer_id) as orders_per_customer,
            -- Fulfillment metrics
            avg(processing_time) as avg_processing_time,
            avg(fulfillment_time) as avg_fulfillment_time,
            -- Status distribution
            countIf(financial_status = 'paid') / count() * 100 as paid_order_rate,
            countIf(fulfillment_status = 'fulfilled') / count() * 100 as fulfillment_rate
        FROM order_metrics
        GROUP BY date
        ORDER BY date
        """
        
        try:
            # Execute query and get results
            result = self.client.execute_query(query)
            
            # Create DataFrame with explicit column names
            df = pd.DataFrame(result, columns=[
                'date', 'daily_revenue', 'total_discounts', 'average_order_value',
                'discount_rate', 'unique_customers', 'total_orders', 'orders_per_customer',
                'avg_processing_time', 'avg_fulfillment_time', 'paid_order_rate',
                'fulfillment_rate'
            ])
            
            # Debug logging to check column names
            logger.info(f"Business Performance DataFrame columns: {df.columns.tolist()}")
            
            # Create visualization
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=(
                    "Daily Revenue & Discounts",
                    "Average Order Value Trend",
                    "Customer Metrics",
                    "Fulfillment Performance",
                    "Order Status Distribution",
                    "Revenue Metrics"
                )
            )
            
            # Revenue and Discounts
            fig.add_trace(
                go.Bar(
                    x=df['date'],
                    y=df['daily_revenue'],
                    name="Daily Revenue",
                    marker_color='rgb(55, 83, 109)'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    x=df['date'],
                    y=df['total_discounts'],
                    name="Discounts",
                    marker_color='rgb(26, 118, 255)'
                ),
                row=1, col=1
            )
            
            # Average Order Value
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['average_order_value'],
                    name="AOV",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=1, col=2
            )
            
            # Customer Metrics
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['unique_customers'],
                    name="Unique Customers",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['orders_per_customer'],
                    name="Orders per Customer",
                    mode='lines+markers',
                    line=dict(color='rgb(255, 65, 54)')
                ),
                row=2, col=1
            )
            
            # Fulfillment Performance
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['avg_processing_time'],
                    name="Processing Time",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=2, col=2
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['avg_fulfillment_time'],
                    name="Fulfillment Time",
                    mode='lines+markers',
                    line=dict(color='rgb(255, 65, 54)')
                ),
                row=2, col=2
            )
            
            # Status Distribution
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['paid_order_rate'],
                    name="Paid Order Rate",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['fulfillment_rate'],
                    name="Fulfillment Rate",
                    mode='lines+markers',
                    line=dict(color='rgb(255, 65, 54)')
                ),
                row=3, col=1
            )
            
            # Revenue Metrics
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['discount_rate'],
                    name="Discount Rate",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=3, col=2
            )
            
            fig.update_layout(
                title_text="Business Performance Dashboard",
                height=1200,
                showlegend=True,
                barmode='group'
            )
            
            # Update y-axis labels
            fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
            fig.update_yaxes(title_text="Amount ($)", row=1, col=2)
            fig.update_yaxes(title_text="Count", row=2, col=1)
            fig.update_yaxes(title_text="Hours", row=2, col=2)
            fig.update_yaxes(title_text="Percentage (%)", row=3, col=1)
            fig.update_yaxes(title_text="Percentage (%)", row=3, col=2)
            
            # Log key insights
            logger.info("Business Performance Insights:")
            logger.info(f"Average Order Value: ${df['average_order_value'].mean():.2f}")
            logger.info(f"Average Discount Rate: {df['discount_rate'].mean():.2f}%")
            logger.info(f"Average Orders per Customer: {df['orders_per_customer'].mean():.2f}")
            logger.info(f"Average Paid Order Rate: {df['paid_order_rate'].mean():.2f}%")
            logger.info(f"Average Fulfillment Rate: {df['fulfillment_rate'].mean():.2f}%")
            
            return df, fig
            
        except Exception as e:
            logger.error(f"Error in business performance metrics: {str(e)}")
            logger.error(f"DataFrame columns: {df.columns.tolist() if 'df' in locals() else 'No DataFrame'}")
            raise

    def get_customer_retention_metrics(self) -> Tuple[pd.DataFrame, go.Figure]:
        """Analyze customer retention and loyalty metrics"""
        query = """
        WITH customer_orders AS (
            SELECT 
                customer_id,
                toDate(created_at) as order_date,
                total_price as order_value,
                row_number() OVER (PARTITION BY customer_id ORDER BY created_at) as order_number
            FROM orders
            WHERE created_at >= now() - INTERVAL 365 DAY
        ),
        retention_metrics AS (
            SELECT 
                order_date,
                count(DISTINCT customer_id) as total_customers,
                count(DISTINCT CASE WHEN order_number = 1 THEN customer_id END) as new_customers,
                count(DISTINCT CASE WHEN order_number > 1 THEN customer_id END) as returning_customers,
                avg(CASE WHEN order_number > 1 THEN order_value END) as returning_customer_value
            FROM customer_orders
            GROUP BY order_date
        )
        SELECT 
            order_date,
            total_customers,
            new_customers,
            returning_customers,
            returning_customer_value,
            (returning_customers / total_customers) * 100 as retention_rate,
            (new_customers / total_customers) * 100 as new_customer_rate
        FROM retention_metrics
        ORDER BY order_date
        """
        
        try:
            # Execute query and get results
            result = self.client.execute_query(query)
            
            # Create DataFrame with explicit column names
            df = pd.DataFrame(result, columns=[
                'order_date', 'total_customers', 'new_customers', 'returning_customers',
                'returning_customer_value', 'retention_rate', 'new_customer_rate'
            ])
            
            # Debug logging to check column names
            logger.info(f"Customer Retention DataFrame columns: {df.columns.tolist()}")
            
            # Create visualization
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    "Customer Acquisition vs Retention",
                    "Customer Retention Rate",
                    "Returning Customer Value",
                    "Customer Growth"
                )
            )
            
            # Customer Acquisition vs Retention
            fig.add_trace(
                go.Bar(
                    x=df['order_date'],
                    y=df['new_customers'],
                    name="New Customers",
                    marker_color='rgb(55, 83, 109)'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    x=df['order_date'],
                    y=df['returning_customers'],
                    name="Returning Customers",
                    marker_color='rgb(26, 118, 255)'
                ),
                row=1, col=1
            )
            
            # Retention Rate
            fig.add_trace(
                go.Scatter(
                    x=df['order_date'],
                    y=df['retention_rate'],
                    name="Retention Rate",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=1, col=2
            )
            
            # Returning Customer Value
            fig.add_trace(
                go.Scatter(
                    x=df['order_date'],
                    y=df['returning_customer_value'],
                    name="Returning Customer Value",
                    mode='lines+markers',
                    line=dict(color='rgb(255, 65, 54)')
                ),
                row=2, col=1
            )
            
            # Customer Growth
            fig.add_trace(
                go.Scatter(
                    x=df['order_date'],
                    y=df['total_customers'],
                    name="Total Customers",
                    mode='lines+markers',
                    line=dict(color='rgb(49, 130, 189)')
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title_text="Customer Retention Analysis",
                height=800,
                showlegend=True,
                barmode='group'
            )
            
            # Update y-axis labels
            fig.update_yaxes(title_text="Number of Customers", row=1, col=1)
            fig.update_yaxes(title_text="Percentage (%)", row=1, col=2)
            fig.update_yaxes(title_text="Average Order Value ($)", row=2, col=1)
            fig.update_yaxes(title_text="Total Customers", row=2, col=2)
            
            # Log key insights
            logger.info("Customer Retention Insights:")
            logger.info(f"Average Retention Rate: {df['retention_rate'].mean():.2f}%")
            logger.info(f"Average New Customer Rate: {df['new_customer_rate'].mean():.2f}%")
            logger.info(f"Average Returning Customer Value: ${df['returning_customer_value'].mean():.2f}")
            
            return df, fig
            
        except Exception as e:
            logger.error(f"Error in customer retention metrics: {str(e)}")
            logger.error(f"DataFrame columns: {df.columns.tolist() if 'df' in locals() else 'No DataFrame'}")
            raise

    def generate_analytics_report(self) -> Dict[str, Tuple[pd.DataFrame, go.Figure]]:
        """Generate a comprehensive analytics report"""
        return {
            'sales_over_time': self.get_sales_over_time(),
            'product_performance': self.get_product_performance(),
            'customer_segments': self.get_customer_segments(),
            'payment_analytics': self.get_payment_analytics(),
            'geographic_analysis': self.get_geographic_analysis(),
            'time_based_metrics': self.get_time_based_metrics(),
            'discount_analysis': self.get_discount_analysis(),
            'product_category_analysis': self.get_product_category_analysis(),
            'customer_lifetime_value': self.get_customer_lifetime_value(),
            'inventory_turnover': self.get_inventory_turnover(),
            'seasonal_trends': self.get_seasonal_trends(),
            'order_aging_analysis': self.get_order_aging_analysis(),
            'order_aging_trends': self.get_order_aging_trends(),
            'business_performance': self.get_business_performance_metrics(),
            'customer_retention': self.get_customer_retention_metrics()
        }