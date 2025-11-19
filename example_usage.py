"""
Example usage of the DGA Report Generator
Demonstrates how to create reports from different data sources
"""

from report_generator import DGAReportGenerator
import json

def example_1_csv_file():
    """Example 1: Generate report from CSV file"""
    print("=" * 60)
    print("Example 1: Generating report from CSV file")
    print("=" * 60)
    
    generator = DGAReportGenerator('sample_data.csv')
    generator.generate_full_report(output_dir='reports/example1')
    print()


def example_2_json_data():
    """Example 2: Generate report from JSON data"""
    print("=" * 60)
    print("Example 2: Generating report from JSON data")
    print("=" * 60)
    
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
    
    json_data = json.dumps(data)
    generator = DGAReportGenerator(json_data)
    generator.generate_full_report(output_dir='reports/example2')
    print()


def example_3_critical_levels():
    """Example 3: Generate report with critical gas levels"""
    print("=" * 60)
    print("Example 3: Generating report with CRITICAL levels")
    print("=" * 60)
    
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
    
    json_data = json.dumps(data)
    generator = DGAReportGenerator(json_data)
    generator.generate_full_report(output_dir='reports/example3')
    print()


def example_4_markdown_only():
    """Example 4: Generate only markdown report"""
    print("=" * 60)
    print("Example 4: Generating markdown report only")
    print("=" * 60)
    
    generator = DGAReportGenerator('sample_data.csv')
    generator.generate_full_report(output_dir='reports/example4', formats=['markdown'])
    print()


if __name__ == "__main__":
    print("\n🔧 DGA Report Generator - Example Usage\n")
    
    # Run examples
    try:
        example_1_csv_file()
        example_2_json_data()
        example_3_critical_levels()
        example_4_markdown_only()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\nCheck the 'reports/' directory for generated reports.")
        
    except FileNotFoundError:
        print("⚠️  Note: Some examples require 'sample_data.csv' to exist.")
        print("    Run example 2 or 3 to see reports from JSON data.")
