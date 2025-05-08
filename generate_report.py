import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.analytics.base.report_generator import AnalyticsReportGenerator

def main():
    """Generate the analytics report"""
    generator = AnalyticsReportGenerator()
    output_path = os.path.join(project_root, "analytics_report.html")
    generator.save_report(output_path)
    print(f"Report generated successfully at: {output_path}")

if __name__ == "__main__":
    main() 