import os
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from src.database.clickhouse_client import ClickHouseClient
from src.analytics.shopify_analytics import ShopifyAnalytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_output_directory():
    """Create output directory for analytics results"""
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "analytics_results"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def save_visualization(fig, filename, output_dir):
    """Save visualization to HTML file"""
    output_path = os.path.join(output_dir, filename)
    fig.write_html(output_path)
    logger.info(f"Saved visualization to {output_path}")

def main():
    try:
        # Initialize ClickHouse client
        client = ClickHouseClient()
        
        # Initialize analytics
        analytics = ShopifyAnalytics(client)
        
        # Create output directory
        output_dir = setup_output_directory()
        logger.info(f"Created output directory: {output_dir}")
        
        # Generate analytics report
        report = analytics.generate_analytics_report()
        
        # Save visualizations and print summary statistics
        for metric_name, (df, fig) in report.items():
            # Save visualization
            save_visualization(fig, f"{metric_name}.html", output_dir)
            
            # Print summary statistics
            logger.info(f"\n{metric_name.upper()} Summary:")
            logger.info("-" * 50)
            logger.info(f"Data shape: {df.shape}")
            logger.info("\nSummary statistics:")
            logger.info(df.describe())
            
            # Save data to CSV
            csv_path = os.path.join(output_dir, f"{metric_name}.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Saved data to {csv_path}")
        
        logger.info(f"\nAnalytics report generated successfully in {output_dir}")
        
    except Exception as e:
        logger.error(f"Error generating analytics report: {str(e)}")
        raise

if __name__ == "__main__":
    main() 