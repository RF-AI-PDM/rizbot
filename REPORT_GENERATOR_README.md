# 📊 DGA Report Generator - User Guide

## Overview

The DGA (Dissolved Gas Analysis) Report Generator is a Python-based tool for creating comprehensive analysis reports from transformer gas monitoring data. It helps maintenance teams quickly assess transformer health and make informed decisions based on IEEE C57.104 standards.

## Features

✅ **Multiple Data Sources**
- Load data from CSV files
- Parse JSON data strings
- Support for multiple measurement points

✅ **Automatic Analysis**
- Gas level threshold checking (Normal, Warning, Critical)
- Statistical analysis (min, max, mean, std dev)
- IEEE C57.104 standard compliance

✅ **Multiple Report Formats**
- Markdown (.md) - Easy to read and version control
- HTML (.html) - Professional web-based reports with styling
- Visual charts (PNG) - Gas concentration trends and status overview

✅ **Visualizations**
- Gas concentration comparison charts
- Status distribution pie charts
- Trend analysis for time-series data

✅ **Actionable Recommendations**
- Automatic recommendations based on analysis results
- Severity-based action items
- Maintenance scheduling suggestions

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- pandas (data manipulation)
- matplotlib (charting)
- seaborn (enhanced visualizations)
- reportlab (PDF support - future)
- jinja2 (template support)
- numpy (numerical operations)

## Quick Start

### 1. Basic Usage - CSV File

```python
from report_generator import DGAReportGenerator

# Create generator with CSV file
generator = DGAReportGenerator('sample_data.csv')

# Generate complete report
generator.generate_full_report(output_dir='reports')
```

### 2. Command Line Usage

```bash
# Generate report from CSV file
python report_generator.py sample_data.csv

# Specify output directory
python report_generator.py sample_data.csv -o my_reports

# Generate only markdown format
python report_generator.py sample_data.csv -f markdown

# Generate both formats (default)
python report_generator.py sample_data.csv -f markdown html
```

### 3. Using JSON Data

```python
import json
from report_generator import DGAReportGenerator

# Prepare your data
data = {
    'H2': [150, 180, 220],
    'CH4': [200, 250, 300],
    'C2H6': [80, 95, 110],
    'C2H4': [60, 75, 90],
    'C2H2': [3, 5, 8],
    'CO': [450, 520, 600],
    'CO2': [3500, 4200, 5000]
}

# Convert to JSON string
json_data = json.dumps(data)

# Generate report
generator = DGAReportGenerator(json_data)
generator.generate_full_report()
```

## Data Format

### CSV Format

Your CSV file should contain columns for the gases you want to analyze:

```csv
timestamp,H2,CH4,C2H6,C2H4,C2H2,CO,CO2,transformer_id,location
2024-01-15 10:00,85,95,45,38,0.5,280,2100,T-001,Plant A
2024-02-15 10:00,92,110,52,42,0.8,310,2250,T-001,Plant A
```

**Required Gas Columns** (at least one):
- H2 (Hydrogen)
- CH4 (Methane)
- C2H6 (Ethane)
- C2H4 (Ethylene)
- C2H2 (Acetylene)
- CO (Carbon Monoxide)
- CO2 (Carbon Dioxide)

**Optional Columns**:
- timestamp (for trend analysis)
- transformer_id (identification)
- location (plant/site name)
- any other metadata

**Unit**: All gas concentrations should be in **ppm (parts per million)**

### JSON Format

```json
{
    "H2": [150, 180, 220],
    "CH4": [200, 250, 300],
    "C2H6": [80, 95, 110],
    "C2H4": [60, 75, 90],
    "C2H2": [3, 5, 8],
    "CO": [450, 520, 600],
    "CO2": [3500, 4200, 5000]
}
```

## Gas Thresholds (IEEE C57.104)

| Gas | Normal (ppm) | Warning (ppm) | Critical (ppm) |
|-----|--------------|---------------|----------------|
| H2  | < 100        | 100 - 700     | > 700          |
| CH4 | < 120        | 120 - 400     | > 400          |
| C2H6| < 65         | 65 - 100      | > 100          |
| C2H4| < 50         | 50 - 100      | > 100          |
| C2H2| < 1          | 1 - 9         | > 9            |
| CO  | < 350        | 350 - 570     | > 570          |
| CO2 | < 2500       | 2500 - 7000   | > 7000         |

## Examples

Run the example script to see different use cases:

```bash
python example_usage.py
```

This will generate:
- Example 1: Report from CSV file
- Example 2: Report from JSON data
- Example 3: Report with critical gas levels
- Example 4: Markdown-only report

## Output Structure

After running the generator, you'll find:

```
reports/
├── report.md              # Markdown report
├── report.html            # HTML report (styled, print-ready)
├── gas_levels.png         # Gas concentration chart
└── status_overview.png    # Status pie chart
```

## Advanced Usage

### Step-by-Step Report Generation

```python
from report_generator import DGAReportGenerator

# 1. Create generator
generator = DGAReportGenerator()

# 2. Load data
generator.load_data('your_data.csv')

# 3. Analyze
analysis = generator.analyze_gas_levels()
print(analysis)

# 4. Generate visualizations
charts = generator.generate_visualizations('output_folder')

# 5. Generate specific format
generator.generate_markdown_report('output/report.md')
generator.generate_html_report('output/report.html')
```

### Custom Output Directory

```python
generator = DGAReportGenerator('data.csv')
generator.generate_full_report(
    output_dir='monthly_reports/2024-01',
    formats=['markdown', 'html']
)
```

## Report Contents

Each report includes:

### 1. Executive Summary
- Overall status (Normal/Warning/Critical)
- Alert counts
- Key findings

### 2. Data Overview
- Number of samples
- Parameters measured
- Analysis date/time

### 3. Critical Alerts
- Gases exceeding critical thresholds
- Current values vs. thresholds
- Immediate action items

### 4. Warnings
- Gases exceeding warning thresholds
- Trend information
- Monitoring recommendations

### 5. Detailed Analysis
- Statistical summary for each gas
- Min, max, mean, standard deviation
- Comparison tables

### 6. Visualizations
- Gas concentration trends
- Status distribution charts
- Color-coded indicators

### 7. Recommendations
- Severity-based action plans
- Maintenance scheduling
- Monitoring frequency

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError`
```
Solution: pip install -r requirements.txt
```

**Issue**: `No data loaded` error
```
Solution: Make sure your CSV file exists and has the correct format
```

**Issue**: Charts not appearing in HTML report
```
Solution: Ensure visualizations are generated before HTML report
          Use generate_full_report() instead of individual functions
```

**Issue**: Empty report or no analysis
```
Solution: Check that your CSV contains at least one gas column (H2, CH4, etc.)
          Verify gas concentration values are numeric (not text)
```

## Best Practices

1. **Regular Monitoring**: Generate reports monthly or quarterly
2. **Trend Analysis**: Include multiple time points in your data
3. **Data Quality**: Ensure measurements are accurate and properly calibrated
4. **Action Items**: Follow recommendations based on severity
5. **Documentation**: Keep generated reports for historical reference

## Integration Ideas

- **Scheduled Reports**: Use cron/scheduler to auto-generate reports
- **Email Alerts**: Send HTML reports via email for critical conditions
- **Dashboard**: Embed charts in monitoring dashboards
- **API Integration**: Connect to SCADA/IoT systems for real-time data
- **Database Storage**: Store analysis results in database for trending

## Support & Contribution

For issues, improvements, or questions:
- Check existing documentation
- Review example_usage.py for working examples
- Consult IEEE C57.104 standard for gas analysis details

## License

This tool follows the repository license (see LICENSE file).

---

**Note**: This report generator is based on IEEE C57.104 standards. Always consult with qualified electrical engineers for critical transformer maintenance decisions.
