# Configuration Search Tool

## Overview

The Configuration Search Tool (`config_search.py`) is a utility designed to scan through the Rizbot project files to identify configuration settings, hardcoded values, file paths, and potential sensitive information.

## Purpose

This tool helps developers and maintainers:
- Identify hardcoded configuration values that should be externalized
- Locate file paths that may need to be made configurable
- Detect potential API keys, secrets, or credentials
- Find environment variable usage
- Discover configuration patterns across the codebase

## Usage

### Basic Usage

Run the tool from the project root directory:

```bash
python3 config_search.py
```

### Specify a Different Directory

You can specify a different project directory to scan:

```bash
python3 config_search.py /path/to/project
```

## Output

The tool produces two types of output:

1. **Console Report**: A formatted report printed to the console with sections for:
   - 📁 File Paths Found
   - 💾 Hardcoded Values Found
   - ⚠️ Potential Credentials/Sensitive Data
   - 🌍 Environment Variables
   - ⚙️ Configuration Patterns
   - Summary statistics

2. **JSON File**: Results are saved to `config_search_results.json` for programmatic access

## What It Searches For

### In Python Files (.py)

- **File Paths**: Hardcoded file or directory paths (e.g., `'/home/user/file.txt'`)
- **Potential Credentials**: Keywords like `api_key`, `secret`, `password`, `token`, `credential`, `auth`
- **File Open Calls**: Calls to `open()` function with file paths
- **Environment Variables**: Usage of `os.environ` or `os.getenv`
- **Configuration Variables**: Variables or patterns suggesting configuration (e.g., `config`, `settings`, `api_url`, `endpoint`)

### In JSON Files (.json)

- **Configuration Keys**: Keys containing words like `config`, `settings`, `api`, `url`, `key`, `path`, `endpoint`
- **URLs**: Any HTTP/HTTPS URLs in string values
- **Data Structure**: Analysis of JSON structure and key patterns

## Example Output

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
  Line 45: intents = load_intents('/home/runner/work/rizbot/rizbot/intents.json')

======================================================================
SUMMARY
======================================================================
Total File Paths: 1
Total Hardcoded Values: 0
Total Potential Credentials: 0
Total Environment Variables: 0
Total Configuration Patterns: 0
======================================================================

💾 Results saved to: config_search_results.json
```

## Current Findings

As of the latest scan of the Rizbot project:

### Identified Configuration Issues

1. **Hardcoded File Path in demo_chatbot.py (Line 45)**
   ```python
   intents = load_intents('/home/runner/work/rizbot/rizbot/intents.json')
   ```
   
   **Recommendation**: This absolute path should be made relative or configurable:
   ```python
   # Option 1: Relative path
   intents = load_intents('intents.json')
   
   # Option 2: Use Path and __file__
   from pathlib import Path
   script_dir = Path(__file__).parent
   intents = load_intents(script_dir / 'intents.json')
   
   # Option 3: Make it configurable
   import os
   intents_path = os.getenv('INTENTS_FILE', 'intents.json')
   intents = load_intents(intents_path)
   ```

## Excluded Files and Directories

The tool automatically excludes:
- **Directories**: `.git`, `__pycache__`, `venv`, `node_modules`, `.venv`
- **Files**: `config_search.py` (itself), `config_search_results.json`

## Integration with Development Workflow

### Recommended Usage

1. **Before Deployment**: Run the tool to identify any hardcoded values that should be externalized
2. **During Code Review**: Check for newly added configuration patterns
3. **Security Audit**: Identify potential credentials or sensitive information
4. **Configuration Migration**: When moving from hardcoded to external configuration

### CI/CD Integration

You can integrate this tool into your CI/CD pipeline:

```bash
# Run the configuration search
python3 config_search.py

# Check if sensitive patterns were found (example)
if [ -f config_search_results.json ]; then
    # Parse JSON and fail build if credentials are found
    python3 -c "
import json
with open('config_search_results.json') as f:
    results = json.load(f)
if results['potential_credentials']:
    print('WARNING: Potential credentials found!')
    exit(1)
"
fi
```

## Customization

You can extend the tool by modifying the patterns in the `ConfigurationSearcher` class:

```python
patterns = {
    'file_paths': r'["\']([/\\][\w/\\.-]+|[\w]+[/\\][\w/\\.-]+)["\']',
    'potential_keys': r'(?i)(api[_-]?key|secret|password|token|credential|auth)',
    # Add your own patterns here
}
```

## Future Enhancements

Potential improvements for the tool:
- Support for YAML configuration files
- Command-line options for custom exclusions
- Integration with secrets management systems
- Automatic fix suggestions
- Configuration file generation
- Support for .env files
- Pattern customization via configuration file

## Contributing

When adding new features or patterns to detect, ensure:
1. The pattern is well-tested
2. Documentation is updated
3. False positives are minimized
4. The tool remains performant

## License

This tool is part of the Rizbot project and follows the same MIT License.
