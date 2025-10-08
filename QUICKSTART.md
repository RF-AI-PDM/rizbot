# Configuration Search Tool - Quick Start Guide

## What is this?

The Configuration Search Tool helps you find configuration-related code in your project, including:
- Hardcoded file paths
- API keys and credentials  
- Environment variables
- Configuration patterns

## Quick Start

### 1. Run the tool

```bash
cd /home/runner/work/rizbot/rizbot
python3 config_search.py
```

### 2. View the results

The tool will:
- Print a detailed report to your console
- Save results to `config_search_results.json`

### 3. Example output

```
🔍 Configuration Search Tool
Project Root: /home/runner/work/rizbot/rizbot

Scanning project at: /home/runner/work/rizbot/rizbot
======================================================================

📄 Found 1 Python file(s)
Analyzing: demo_chatbot.py

📋 Found 1 JSON file(s)
Analyzing: intents.json

======================================================================
CONFIGURATION SEARCH REPORT
======================================================================

📁 File Paths Found (1):
----------------------------------------------------------------------
  File: demo_chatbot.py
  Line 60: print("\n" + "="*50)

======================================================================
SUMMARY
======================================================================
Total File Paths: 1
Total Hardcoded Values: 0
Total Potential Credentials: 0
Total Environment Variables: 0
Total Configuration Patterns: 0
======================================================================
```

## What We Fixed

### Before
```python
# demo_chatbot.py (Line 45) - Hardcoded absolute path
intents = load_intents('/home/runner/work/rizbot/rizbot/intents.json')
```

### After
```python
# demo_chatbot.py - Now uses relative path
from pathlib import Path

script_dir = Path(__file__).parent
intents_file = script_dir / 'intents.json'
intents = load_intents(intents_file)
```

## Why This Matters

✅ **Portability**: Code works on any machine, not just one specific path
✅ **Maintainability**: Easy to move files around without breaking code
✅ **Security**: Helps identify potential hardcoded credentials
✅ **Best Practices**: Follows Python conventions for path handling

## Next Steps

1. Review the CONFIG_SEARCH_README.md for detailed documentation
2. Run the tool periodically during development
3. Consider integrating it into your CI/CD pipeline

## Need Help?

See the full documentation: [CONFIG_SEARCH_README.md](CONFIG_SEARCH_README.md)
