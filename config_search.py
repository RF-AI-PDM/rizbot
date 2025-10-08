#!/usr/bin/env python3
"""
Configuration Search Tool for Rizbot Project

This tool searches through project files to identify configuration settings,
hardcoded values, file paths, and potential sensitive information.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple


class ConfigurationSearcher:
    """Searches for configuration patterns in project files"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results = {
            'file_paths': [],
            'hardcoded_values': [],
            'potential_credentials': [],
            'environment_variables': [],
            'configuration_patterns': []
        }
    
    def search_python_file(self, filepath: Path) -> Dict[str, List[Tuple[int, str]]]:
        """Search for configuration patterns in Python files"""
        patterns = {
            'file_paths': r'["\']([/\\][\w/\\.-]+|[\w]+[/\\][\w/\\.-]+)["\']',
            'potential_keys': r'(?i)(api[_-]?key|secret|password|token|credential|auth)',
            'open_calls': r'open\s*\(["\']([^"\']+)["\']',
            'env_vars': r'os\.(?:environ|getenv)\s*\[?["\']([^"\']+)["\']?\]?',
            'config_vars': r'(?i)(config|settings|api_url|base_url|endpoint)',
        }
        
        findings = {key: [] for key in patterns.keys()}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        findings[pattern_name].append((line_num, line.strip()))
        
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        
        return findings
    
    def search_json_file(self, filepath: Path) -> Dict[str, List]:
        """Search for configuration patterns in JSON files"""
        findings = {
            'keys': [],
            'potential_config': [],
            'urls': []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Recursively search for configuration-like keys
            def search_dict(obj, path=''):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        
                        # Check for configuration-like keys
                        if any(keyword in key.lower() for keyword in 
                               ['config', 'settings', 'api', 'url', 'key', 'path', 'endpoint']):
                            findings['potential_config'].append({
                                'path': current_path,
                                'key': key,
                                'value_type': type(value).__name__
                            })
                        
                        # Check for URLs
                        if isinstance(value, str) and (value.startswith('http://') or 
                                                       value.startswith('https://')):
                            findings['urls'].append({
                                'path': current_path,
                                'url': value
                            })
                        
                        search_dict(value, current_path)
                
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        search_dict(item, f"{path}[{i}]")
            
            search_dict(data)
            findings['keys'] = list(data.keys()) if isinstance(data, dict) else []
        
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        
        return findings
    
    def scan_project(self, excluded_dirs: List[str] = None, excluded_files: List[str] = None) -> Dict:
        """Scan all project files for configuration patterns"""
        if excluded_dirs is None:
            excluded_dirs = ['.git', '__pycache__', 'venv', 'node_modules', '.venv']
        
        if excluded_files is None:
            excluded_files = ['config_search.py', 'config_search_results.json']
        
        print(f"Scanning project at: {self.project_root}")
        print("=" * 70)
        
        # Find all Python and JSON files
        python_files = []
        json_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Exclude certain directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                # Skip excluded files
                if file in excluded_files:
                    continue
                    
                filepath = Path(root) / file
                if file.endswith('.py'):
                    python_files.append(filepath)
                elif file.endswith('.json'):
                    json_files.append(filepath)
        
        # Scan Python files
        print(f"\n📄 Found {len(python_files)} Python file(s)")
        for py_file in python_files:
            print(f"\nAnalyzing: {py_file.relative_to(self.project_root)}")
            findings = self.search_python_file(py_file)
            
            # Store results
            for pattern_name, matches in findings.items():
                if matches:
                    for line_num, line_content in matches:
                        result_entry = {
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': line_num,
                            'content': line_content,
                            'pattern': pattern_name
                        }
                        
                        if pattern_name == 'file_paths':
                            self.results['file_paths'].append(result_entry)
                        elif pattern_name == 'potential_keys':
                            self.results['potential_credentials'].append(result_entry)
                        elif pattern_name == 'env_vars':
                            self.results['environment_variables'].append(result_entry)
                        else:
                            self.results['configuration_patterns'].append(result_entry)
        
        # Scan JSON files
        print(f"\n📋 Found {len(json_files)} JSON file(s)")
        for json_file in json_files:
            print(f"\nAnalyzing: {json_file.relative_to(self.project_root)}")
            findings = self.search_json_file(json_file)
            
            if findings['potential_config']:
                for config in findings['potential_config']:
                    self.results['configuration_patterns'].append({
                        'file': str(json_file.relative_to(self.project_root)),
                        'type': 'json_key',
                        'path': config['path'],
                        'key': config['key'],
                        'value_type': config['value_type']
                    })
            
            if findings['urls']:
                for url_info in findings['urls']:
                    self.results['hardcoded_values'].append({
                        'file': str(json_file.relative_to(self.project_root)),
                        'type': 'url',
                        'path': url_info['path'],
                        'value': url_info['url']
                    })
        
        return self.results
    
    def print_report(self):
        """Print a formatted report of findings"""
        print("\n" + "=" * 70)
        print("CONFIGURATION SEARCH REPORT")
        print("=" * 70)
        
        # File Paths
        if self.results['file_paths']:
            print(f"\n📁 File Paths Found ({len(self.results['file_paths'])}):")
            print("-" * 70)
            for item in self.results['file_paths']:
                print(f"  File: {item['file']}")
                print(f"  Line {item['line']}: {item['content']}")
                print()
        else:
            print("\n📁 File Paths Found: None")
        
        # Hardcoded Values
        if self.results['hardcoded_values']:
            print(f"\n💾 Hardcoded Values Found ({len(self.results['hardcoded_values'])}):")
            print("-" * 70)
            for item in self.results['hardcoded_values']:
                print(f"  File: {item['file']}")
                print(f"  Type: {item['type']}")
                if 'path' in item:
                    print(f"  Path: {item['path']}")
                if 'value' in item:
                    print(f"  Value: {item['value']}")
                print()
        else:
            print("\n💾 Hardcoded Values Found: None")
        
        # Potential Credentials
        if self.results['potential_credentials']:
            print(f"\n⚠️  Potential Credentials/Sensitive Data ({len(self.results['potential_credentials'])}):")
            print("-" * 70)
            for item in self.results['potential_credentials']:
                print(f"  File: {item['file']}")
                print(f"  Line {item['line']}: {item['content']}")
                print()
        else:
            print("\n⚠️  Potential Credentials/Sensitive Data: None")
        
        # Environment Variables
        if self.results['environment_variables']:
            print(f"\n🌍 Environment Variables ({len(self.results['environment_variables'])}):")
            print("-" * 70)
            for item in self.results['environment_variables']:
                print(f"  File: {item['file']}")
                print(f"  Line {item['line']}: {item['content']}")
                print()
        else:
            print("\n🌍 Environment Variables: None")
        
        # Configuration Patterns
        if self.results['configuration_patterns']:
            print(f"\n⚙️  Configuration Patterns ({len(self.results['configuration_patterns'])}):")
            print("-" * 70)
            for item in self.results['configuration_patterns']:
                print(f"  File: {item['file']}")
                if 'line' in item:
                    print(f"  Line {item['line']}: {item['content']}")
                elif 'path' in item:
                    print(f"  JSON Path: {item['path']}")
                    print(f"  Key: {item['key']}")
                    print(f"  Value Type: {item['value_type']}")
                print()
        else:
            print("\n⚙️  Configuration Patterns: None")
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total File Paths: {len(self.results['file_paths'])}")
        print(f"Total Hardcoded Values: {len(self.results['hardcoded_values'])}")
        print(f"Total Potential Credentials: {len(self.results['potential_credentials'])}")
        print(f"Total Environment Variables: {len(self.results['environment_variables'])}")
        print(f"Total Configuration Patterns: {len(self.results['configuration_patterns'])}")
        print("=" * 70)


def main():
    """Main entry point for the configuration search tool"""
    import sys
    
    # Get project root from command line or use current directory
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    print("🔍 Configuration Search Tool")
    print(f"Project Root: {project_root}\n")
    
    searcher = ConfigurationSearcher(project_root)
    searcher.scan_project()
    searcher.print_report()
    
    # Optionally save results to JSON
    output_file = 'config_search_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(searcher.results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
