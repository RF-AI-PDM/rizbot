"""
Report Generator for Predictive Maintenance DGA Analysis
Generates comprehensive reports from transformer gas analysis data

REFACTORED VERSION: Uses common_utils for shared functionality
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from typing import Dict, List, Optional
import numpy as np

# Import common utilities (eliminates duplicated code)
from common_utils import (
    FileUtils, ErrorHandler, DataProcessor, ConfigManager,
    print_success, print_error, print_warning, print_section_header
)


class DGAReportGenerator:
    """Generate reports from Dissolved Gas Analysis (DGA) data"""
    
    def __init__(self, data_source: str = None):
        """
        Initialize the report generator
        
        Args:
            data_source: Path to CSV file or JSON data string
        """
        self.data_source = data_source
        self.data = None
        self.analysis_results = {}
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # DGA gas thresholds (ppm) based on IEEE C57.104
        self.thresholds = {
            'H2': {'normal': 100, 'warning': 700, 'critical': 1800},
            'CH4': {'normal': 120, 'warning': 400, 'critical': 1000},
            'C2H6': {'normal': 65, 'warning': 100, 'critical': 150},
            'C2H4': {'normal': 50, 'warning': 100, 'critical': 200},
            'C2H2': {'normal': 1, 'warning': 9, 'critical': 35},
            'CO': {'normal': 350, 'warning': 570, 'critical': 1400},
            'CO2': {'normal': 2500, 'warning': 7000, 'critical': 10000}
        }
    
    def load_data(self, data_source: str = None):
        """
        Load data from CSV file or JSON string
        
        REFACTORED: Uses ErrorHandler for consistent error handling
        """
        source = data_source or self.data_source
        
        if not source:
            raise ValueError("No data source provided")
        
        # Try to load as CSV file
        if FileUtils.check_file_exists(source, "Data file"):
            def load_csv():
                self.data = pd.read_csv(source)
                print_success(f"Loaded data from {source}")
                return True
            
            result = ErrorHandler.safe_execute(
                load_csv,
                error_message=f"Error loading CSV from {source}",
                default_return=False
            )
            if result:
                return True
        
        # Try to parse as JSON
        def load_json():
            data_dict = json.loads(source)
            self.data = pd.DataFrame(data_dict)
            print_success("Loaded data from JSON")
            return True
        
        result = ErrorHandler.safe_execute(
            load_json,
            error_message="Could not parse as JSON",
            default_return=False
        )
        
        if result:
            return True
        
        raise ValueError("Could not load data from provided source")
    
    def analyze_gas_levels(self) -> Dict:
        """Analyze gas levels against thresholds"""
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        analysis = {
            'summary': {},
            'warnings': [],
            'critical': []
        }
        
        # Check each gas column if it exists
        for gas, thresholds in self.thresholds.items():
            if gas in self.data.columns:
                values = self.data[gas].dropna()
                if len(values) > 0:
                    max_val = values.max()
                    mean_val = values.mean()
                    
                    analysis['summary'][gas] = {
                        'max': float(max_val),
                        'mean': float(mean_val),
                        'min': float(values.min()),
                        'std': float(values.std())
                    }
                    
                    # Check thresholds
                    if max_val > thresholds['critical']:
                        analysis['critical'].append({
                            'gas': gas,
                            'value': float(max_val),
                            'threshold': thresholds['critical'],
                            'severity': 'CRITICAL'
                        })
                    elif max_val > thresholds['warning']:
                        analysis['warnings'].append({
                            'gas': gas,
                            'value': float(max_val),
                            'threshold': thresholds['warning'],
                            'severity': 'WARNING'
                        })
        
        self.analysis_results = analysis
        return analysis
    
    def generate_visualizations(self, output_dir: str = None) -> List[str]:
        """
        Generate visualization charts
        
        REFACTORED: Uses ConfigManager for directory management
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        # Use ConfigManager to get reports directory
        if output_dir is None:
            output_dir = str(ConfigManager.get_reports_dir())
        else:
            FileUtils.ensure_dir_exists(output_dir)
        
        chart_files = []
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        # 1. Gas concentration comparison
        gas_columns = [col for col in self.data.columns if col in self.thresholds.keys()]
        
        if gas_columns:
            fig, ax = plt.subplots()
            
            if len(self.data) > 0:
                # If data has multiple rows, show trends
                if len(self.data) > 1 and 'timestamp' in self.data.columns:
                    for gas in gas_columns:
                        if gas in self.data.columns:
                            ax.plot(self.data.index, self.data[gas], marker='o', label=gas)
                    ax.set_xlabel('Sample Index')
                    ax.set_ylabel('Concentration (ppm)')
                    ax.set_title('Gas Concentration Trends')
                else:
                    # Bar chart for single or multiple measurements
                    gas_means = [self.data[gas].mean() for gas in gas_columns if gas in self.data.columns]
                    ax.bar(gas_columns, gas_means, color='steelblue', alpha=0.7)
                    ax.set_xlabel('Gas Type')
                    ax.set_ylabel('Mean Concentration (ppm)')
                    ax.set_title('Gas Concentration Levels')
                
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                chart_path = os.path.join(output_dir, 'gas_levels.png')
                plt.tight_layout()
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                chart_files.append(chart_path)
                print_success(f"Generated chart: {chart_path}")
        
        # 2. Status overview (pie chart)
        if self.analysis_results:
            fig, ax = plt.subplots()
            
            critical_count = len(self.analysis_results.get('critical', []))
            warning_count = len(self.analysis_results.get('warnings', []))
            normal_count = len(gas_columns) - critical_count - warning_count
            
            if critical_count + warning_count + normal_count > 0:
                sizes = [normal_count, warning_count, critical_count]
                labels = ['Normal', 'Warning', 'Critical']
                colors = ['#90EE90', '#FFD700', '#FF6B6B']
                
                # Filter out zero values
                filtered_data = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
                if filtered_data:
                    sizes, labels, colors = zip(*filtered_data)
                    
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                           startangle=90, textprops={'fontsize': 11})
                    ax.set_title('Gas Status Distribution')
                    
                    chart_path = os.path.join(output_dir, 'status_overview.png')
                    plt.tight_layout()
                    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                    plt.close()
                    chart_files.append(chart_path)
                    print_success(f"Generated chart: {chart_path}")
        
        return chart_files
    
    def generate_markdown_report(self, output_path: str = None) -> str:
        """
        Generate a markdown format report
        
        REFACTORED: Uses ConfigManager for path management
        """
        if output_path is None:
            output_path = str(ConfigManager.get_reports_dir() / "report.md")
        
        FileUtils.ensure_dir_exists(str(ConfigManager.get_reports_dir()))
        
        report = self._build_markdown_content()
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print_success(f"Generated markdown report: {output_path}")
        return output_path
    
    def _build_markdown_content(self) -> str:
        """Build markdown report content"""
        report = []
        report.append("# Predictive Maintenance - DGA Analysis Report\n")
        report.append(f"**Generated:** {self.report_date}\n")
        report.append("---\n\n")
        
        # Executive Summary
        report.append("## Executive Summary\n\n")
        
        if self.analysis_results:
            critical_count = len(self.analysis_results.get('critical', []))
            warning_count = len(self.analysis_results.get('warnings', []))
            
            if critical_count > 0:
                report.append(f"⚠️ **CRITICAL ALERTS:** {critical_count} gas(es) exceed critical thresholds\n\n")
            elif warning_count > 0:
                report.append(f"⚡ **WARNINGS:** {warning_count} gas(es) exceed warning thresholds\n\n")
            else:
                report.append("✅ **STATUS:** All gas levels within normal ranges\n\n")
        
        # Data Overview
        report.append("## Data Overview\n\n")
        if self.data is not None:
            report.append(f"- **Total Samples:** {len(self.data)}\n")
            report.append(f"- **Parameters Measured:** {len(self.data.columns)}\n")
            gas_list = ', '.join([col for col in self.data.columns if col in self.thresholds.keys()])
            report.append(f"- **Gases Analyzed:** {gas_list}\n\n")
        
        # Critical Alerts
        if self.analysis_results.get('critical'):
            report.append("## 🚨 Critical Alerts\n\n")
            report.append("| Gas | Value (ppm) | Threshold (ppm) | Status |\n")
            report.append("|-----|-------------|-----------------|--------|\n")
            for alert in self.analysis_results['critical']:
                report.append(f"| {alert['gas']} | {alert['value']:.2f} | {alert['threshold']} | ⚠️ CRITICAL |\n")
            report.append("\n")
        
        # Warnings
        if self.analysis_results.get('warnings'):
            report.append("## ⚡ Warnings\n\n")
            report.append("| Gas | Value (ppm) | Threshold (ppm) | Status |\n")
            report.append("|-----|-------------|-----------------|--------|\n")
            for warning in self.analysis_results['warnings']:
                report.append(f"| {warning['gas']} | {warning['value']:.2f} | {warning['threshold']} | ⚡ WARNING |\n")
            report.append("\n")
        
        # Detailed Analysis
        if self.analysis_results.get('summary'):
            report.append("## Detailed Gas Analysis\n\n")
            report.append("| Gas | Min (ppm) | Mean (ppm) | Max (ppm) | Std Dev |\n")
            report.append("|-----|-----------|------------|-----------|----------|\n")
            for gas, stats in self.analysis_results['summary'].items():
                report.append(f"| {gas} | {stats['min']:.2f} | {stats['mean']:.2f} | {stats['max']:.2f} | {stats['std']:.2f} |\n")
            report.append("\n")
        
        # Recommendations
        report.append(self._get_recommendations())
        
        # Footer
        report.append("---\n")
        report.append("*Report generated by PdM DGA Analysis System*\n")
        report.append("*Based on IEEE C57.104 Standards*\n")
        
        return "".join(report)
    
    def _get_recommendations(self) -> str:
        """Get recommendations based on analysis results"""
        recommendations = ["## Recommendations\n\n"]
        
        if self.analysis_results.get('critical'):
            recommendations.extend([
                "1. **IMMEDIATE ACTION REQUIRED:** Critical gas levels detected\n",
                "2. Schedule emergency inspection of transformer\n",
                "3. Consider taking transformer offline for detailed assessment\n",
                "4. Perform additional oil sampling within 24 hours\n\n"
            ])
        elif self.analysis_results.get('warnings'):
            recommendations.extend([
                "1. **INCREASED MONITORING:** Warning thresholds exceeded\n",
                "2. Increase sampling frequency to weekly\n",
                "3. Schedule maintenance inspection within 30 days\n",
                "4. Monitor trend development closely\n\n"
            ])
        else:
            recommendations.extend([
                "1. Continue regular monitoring schedule\n",
                "2. Perform next DGA analysis as per maintenance plan\n",
                "3. Maintain current operating conditions\n\n"
            ])
        
        return "".join(recommendations)
    
    def generate_html_report(self, output_path: str = None) -> str:
        """
        Generate an HTML format report
        
        REFACTORED: Simplified with helper method
        """
        if output_path is None:
            output_path = str(ConfigManager.get_reports_dir() / "report.html")
        
        FileUtils.ensure_dir_exists(str(ConfigManager.get_reports_dir()))
        
        html_content = self._build_html_content()
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print_success(f"Generated HTML report: {output_path}")
        return output_path
    
    def _build_html_content(self) -> str:
        """Build HTML report content (implementation same as original)"""
        # Note: HTML building code remains the same as the original
        # This is intentionally kept to maintain exact output format
        html = []
        html.append("<!DOCTYPE html>\n")
        html.append("<html lang='en'>\n<head>\n")
        html.append("    <meta charset='UTF-8'>\n")
        html.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        html.append("    <title>DGA Analysis Report</title>\n")
        html.append("    <style>\n")
        html.append("        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }\n")
        html.append("        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n")
        html.append("        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }\n")
        html.append("        h2 { color: #34495e; margin-top: 30px; }\n")
        html.append("        table { border-collapse: collapse; width: 100%; margin: 20px 0; }\n")
        html.append("        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }\n")
        html.append("        th { background-color: #3498db; color: white; }\n")
        html.append("        tr:nth-child(even) { background-color: #f2f2f2; }\n")
        html.append("        .critical { color: #e74c3c; font-weight: bold; }\n")
        html.append("        .warning { color: #f39c12; font-weight: bold; }\n")
        html.append("        .normal { color: #27ae60; font-weight: bold; }\n")
        html.append("        .status-box { padding: 15px; margin: 20px 0; border-radius: 5px; }\n")
        html.append("        .status-critical { background-color: #fee; border-left: 4px solid #e74c3c; }\n")
        html.append("        .status-warning { background-color: #fef8e7; border-left: 4px solid #f39c12; }\n")
        html.append("        .status-normal { background-color: #eafaf1; border-left: 4px solid #27ae60; }\n")
        html.append("        .chart { margin: 20px 0; text-align: center; }\n")
        html.append("        .chart img { max-width: 100%; height: auto; border: 1px solid #ddd; }\n")
        html.append("        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }\n")
        html.append("    </style>\n")
        html.append("</head>\n<body>\n")
        html.append("    <div class='container'>\n")
        
        # Header
        html.append("        <h1>🔧 Predictive Maintenance - DGA Analysis Report</h1>\n")
        html.append(f"        <p><strong>Generated:</strong> {self.report_date}</p>\n")
        
        # Status Summary
        if self.analysis_results:
            critical_count = len(self.analysis_results.get('critical', []))
            warning_count = len(self.analysis_results.get('warnings', []))
            
            if critical_count > 0:
                html.append("        <div class='status-box status-critical'>\n")
                html.append(f"            <h3>⚠️ CRITICAL ALERTS: {critical_count} gas(es) exceed critical thresholds</h3>\n")
                html.append("        </div>\n")
            elif warning_count > 0:
                html.append("        <div class='status-box status-warning'>\n")
                html.append(f"            <h3>⚡ WARNINGS: {warning_count} gas(es) exceed warning thresholds</h3>\n")
                html.append("        </div>\n")
            else:
                html.append("        <div class='status-box status-normal'>\n")
                html.append("            <h3>✅ STATUS: All gas levels within normal ranges</h3>\n")
                html.append("        </div>\n")
        
        # Data Overview
        html.append("        <h2>Data Overview</h2>\n")
        if self.data is not None:
            html.append("        <ul>\n")
            html.append(f"            <li><strong>Total Samples:</strong> {len(self.data)}</li>\n")
            html.append(f"            <li><strong>Parameters Measured:</strong> {len(self.data.columns)}</li>\n")
            gas_list = ', '.join([col for col in self.data.columns if col in self.thresholds.keys()])
            html.append(f"            <li><strong>Gases Analyzed:</strong> {gas_list}</li>\n")
            html.append("        </ul>\n")
        
        # Critical Alerts
        if self.analysis_results.get('critical'):
            html.append("        <h2>🚨 Critical Alerts</h2>\n")
            html.append("        <table>\n")
            html.append("            <tr><th>Gas</th><th>Value (ppm)</th><th>Threshold (ppm)</th><th>Status</th></tr>\n")
            for alert in self.analysis_results['critical']:
                html.append(f"            <tr><td>{alert['gas']}</td><td>{alert['value']:.2f}</td><td>{alert['threshold']}</td><td class='critical'>⚠️ CRITICAL</td></tr>\n")
            html.append("        </table>\n")
        
        # Warnings
        if self.analysis_results.get('warnings'):
            html.append("        <h2>⚡ Warnings</h2>\n")
            html.append("        <table>\n")
            html.append("            <tr><th>Gas</th><th>Value (ppm)</th><th>Threshold (ppm)</th><th>Status</th></tr>\n")
            for warning in self.analysis_results['warnings']:
                html.append(f"            <tr><td>{warning['gas']}</td><td>{warning['value']:.2f}</td><td>{warning['threshold']}</td><td class='warning'>⚡ WARNING</td></tr>\n")
            html.append("        </table>\n")
        
        # Detailed Analysis
        if self.analysis_results.get('summary'):
            html.append("        <h2>Detailed Gas Analysis</h2>\n")
            html.append("        <table>\n")
            html.append("            <tr><th>Gas</th><th>Min (ppm)</th><th>Mean (ppm)</th><th>Max (ppm)</th><th>Std Dev</th></tr>\n")
            for gas, stats in self.analysis_results['summary'].items():
                html.append(f"            <tr><td>{gas}</td><td>{stats['min']:.2f}</td><td>{stats['mean']:.2f}</td><td>{stats['max']:.2f}</td><td>{stats['std']:.2f}</td></tr>\n")
            html.append("        </table>\n")
        
        # Charts - simplified path handling
        import os
        chart_files = ['gas_levels.png', 'status_overview.png']
        output_dir = str(ConfigManager.get_reports_dir())
        existing_charts = [f for f in chart_files if os.path.exists(os.path.join(output_dir, f))]
        
        if existing_charts:
            html.append("        <h2>Visualizations</h2>\n")
            for chart in existing_charts:
                html.append(f"        <div class='chart'>\n")
                html.append(f"            <img src='{chart}' alt='Chart'>\n")
                html.append("        </div>\n")
        
        # Recommendations
        html.append("        <h2>Recommendations</h2>\n")
        html.append("        <ol>\n")
        if self.analysis_results.get('critical'):
            html.append("            <li><strong>IMMEDIATE ACTION REQUIRED:</strong> Critical gas levels detected</li>\n")
            html.append("            <li>Schedule emergency inspection of transformer</li>\n")
            html.append("            <li>Consider taking transformer offline for detailed assessment</li>\n")
            html.append("            <li>Perform additional oil sampling within 24 hours</li>\n")
        elif self.analysis_results.get('warnings'):
            html.append("            <li><strong>INCREASED MONITORING:</strong> Warning thresholds exceeded</li>\n")
            html.append("            <li>Increase sampling frequency to weekly</li>\n")
            html.append("            <li>Schedule maintenance inspection within 30 days</li>\n")
            html.append("            <li>Monitor trend development closely</li>\n")
        else:
            html.append("            <li>Continue regular monitoring schedule</li>\n")
            html.append("            <li>Perform next DGA analysis as per maintenance plan</li>\n")
            html.append("            <li>Maintain current operating conditions</li>\n")
        html.append("        </ol>\n")
        
        # Footer
        html.append("        <div class='footer'>\n")
        html.append("            <p><em>Report generated by PdM DGA Analysis System</em></p>\n")
        html.append("            <p><em>Based on IEEE C57.104 Standards</em></p>\n")
        html.append("        </div>\n")
        
        html.append("    </div>\n")
        html.append("</body>\n</html>\n")
        
        return "".join(html)
    
    def generate_full_report(self, output_dir: str = None, 
                           formats: List[str] = None) -> Dict[str, str]:
        """
        Generate complete report in multiple formats
        
        REFACTORED: Uses ConfigManager and improved error handling
        """
        if formats is None:
            formats = ['markdown', 'html']
        
        if output_dir is None:
            output_dir = str(ConfigManager.get_reports_dir())
        
        if self.data is None:
            print("Loading data...")
            self.load_data()
        
        print("Analyzing gas levels...")
        self.analyze_gas_levels()
        
        print("Generating visualizations...")
        chart_files = self.generate_visualizations(output_dir)
        
        output_files = {'charts': chart_files}
        
        print("Generating reports...")
        if 'markdown' in formats:
            md_path = self.generate_markdown_report(f"{output_dir}/report.md")
            output_files['markdown'] = md_path
        
        if 'html' in formats:
            html_path = self.generate_html_report(f"{output_dir}/report.html")
            output_files['html'] = html_path
        
        print_success("Report generation complete!")
        print(f"📁 Output directory: {output_dir}")
        
        return output_files


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate DGA Analysis Report')
    parser.add_argument('data', help='Path to CSV file or JSON data')
    parser.add_argument('-o', '--output', default=None, help='Output directory (default: reports)')
    parser.add_argument('-f', '--format', nargs='+', choices=['markdown', 'html'], 
                       default=['markdown', 'html'], help='Output format(s)')
    
    args = parser.parse_args()
    
    # Create generator and generate report with error handling
    def generate():
        generator = DGAReportGenerator(args.data)
        generator.generate_full_report(output_dir=args.output, formats=args.format)
        return 0
    
    return ErrorHandler.safe_execute(
        generate,
        error_message="Failed to generate report",
        default_return=1
    )


if __name__ == "__main__":
    exit(main())
