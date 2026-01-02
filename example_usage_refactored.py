"""
Example usage of the DGA Report Generator
Demonstrates how to create reports from different data sources

REFACTORED VERSION: Uses common_utils for shared functionality
"""

from report_generator_refactored import DGAReportGenerator
from common_utils import print_section_header, ErrorHandler
import json


def example_1_csv_file():
    """Example 1: Generate report from CSV file"""
    print_section_header("Example 1: Generating report from CSV file", width=60, char="=")
    
    def generate():
        generator = DGAReportGenerator('sample_data.csv')
        generator.generate_full_report(output_dir='reports/example1')
    
    ErrorHandler.safe_execute(
        generate,
        error_message="Failed to generate report from CSV"
    )
    print()


def example_2_json_data():
    """Example 2: Generate report from JSON data"""
    print_section_header("Example 2: Generating report from JSON data", width=60, char="=")
    
    # Sample JSON data
    data = {
        'H2': [150, 180, 220],
        'CH4': [200, 250, 300],
        'C2H6': [80, 95, 110],
        'C2H4': [60, 75, 90],
        'C2H2': [3, 5, 8],
        'CO': [450, 520, 600],
        'CO2': [3500, 4200, 5000],
        'transformer_id': ['T-002', 'T-002', 'T-002']
    }
    
    def generate():
        json_data = json.dumps(data)
        generator = DGAReportGenerator(json_data)
        generator.generate_full_report(output_dir='reports/example2')
    
    ErrorHandler.safe_execute(
        generate,
        error_message="Failed to generate report from JSON"
    )
    print()


def example_3_critical_levels():
    """Example 3: Generate report with critical gas levels"""
    print_section_header("Example 3: Generating report with CRITICAL levels", width=60, char="=")
    
    # Data with critical gas levels
    data = {
        'H2': [1850, 2000, 2200],
        'CH4': [1100, 1200, 1350],
        'C2H6': [160, 180, 200],
        'C2H4': [220, 250, 280],
        'C2H2': [40, 45, 50],
        'CO': [1500, 1600, 1700],
        'CO2': [11000, 12000, 13000],
        'transformer_id': ['T-003', 'T-003', 'T-003']
    }
    
    def generate():
        json_data = json.dumps(data)
        generator = DGAReportGenerator(json_data)
        generator.generate_full_report(output_dir='reports/example3')
    
    ErrorHandler.safe_execute(
        generate,
        error_message="Failed to generate report with critical levels"
    )
    print()


def example_4_markdown_only():
    """Example 4: Generate only markdown report"""
    print_section_header("Example 4: Generating markdown report only", width=60, char="=")
    
    def generate():
        generator = DGAReportGenerator('sample_data.csv')
        generator.generate_full_report(output_dir='reports/example4', formats=['markdown'])
    
    ErrorHandler.safe_execute(
        generate,
        error_message="Failed to generate markdown report"
    )
    print()


def main():
    """Run all examples"""
    print_section_header("🔧 DGA Report Generator - Example Usage", width=60)
    
    # Run examples
    example_1_csv_file()
    example_2_json_data()
    example_3_critical_levels()
    example_4_markdown_only()
    
    print_section_header("✅ All examples completed successfully!", width=60, char="=")
    print("\nCheck the 'reports/' directory for generated reports.")
    return 0


if __name__ == "__main__":
    exit(main())
