"""
Common Utilities for Rizbot Project
Provides shared functionality across chatbot and report generator modules
"""

import json
import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path


class FileUtils:
    """Utilities for file operations"""
    
    @staticmethod
    def load_json(filename: str, error_context: str = "file") -> Dict[str, Any]:
        """
        Load and parse a JSON file with consistent error handling
        
        Args:
            filename: Path to JSON file
            error_context: Context description for error messages
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            SystemExit: If file cannot be loaded or parsed
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"✓ Loaded {error_context} from {filename}")
            return data
        except FileNotFoundError:
            print(f"Error: {error_context.capitalize()} '{filename}' not found!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {filename}: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to load {error_context} from {filename}: {e}")
            sys.exit(1)
    
    @staticmethod
    def save_json(data: Dict[str, Any], filename: str, indent: int = 2) -> bool:
        """
        Save data to JSON file with error handling
        
        Args:
            data: Data to save
            filename: Output file path
            indent: JSON indentation level
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            print(f"✓ Saved data to {filename}")
            return True
        except Exception as e:
            print(f"Error: Failed to save to {filename}: {e}")
            return False
    
    @staticmethod
    def ensure_dir_exists(directory: str) -> Path:
        """
        Ensure a directory exists, create it if it doesn't
        
        Args:
            directory: Directory path
            
        Returns:
            Path object for the directory
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def check_file_exists(filename: str, description: str = "File") -> bool:
        """
        Check if a file exists with user-friendly message
        
        Args:
            filename: File path to check
            description: Description for error message
            
        Returns:
            True if file exists, False otherwise
        """
        if os.path.exists(filename):
            return True
        else:
            print(f"Error: {description} '{filename}' not found!")
            return False


class ErrorHandler:
    """Centralized error handling utilities"""
    
    @staticmethod
    def handle_file_error(filename: str, error: Exception, operation: str = "process") -> None:
        """
        Handle file-related errors with consistent messaging
        
        Args:
            filename: File that caused the error
            error: Exception object
            operation: Description of operation being performed
        """
        if isinstance(error, FileNotFoundError):
            print(f"✗ Error: File '{filename}' not found")
        elif isinstance(error, PermissionError):
            print(f"✗ Error: Permission denied accessing '{filename}'")
        elif isinstance(error, json.JSONDecodeError):
            print(f"✗ Error: Invalid JSON in '{filename}'")
        else:
            print(f"✗ Error: Failed to {operation} '{filename}': {error}")
    
    @staticmethod
    def safe_execute(func, error_message: str = "Operation failed", 
                    default_return=None, raise_exception: bool = False):
        """
        Execute a function with error handling
        
        Args:
            func: Function to execute
            error_message: Message to display on error
            default_return: Value to return on error
            raise_exception: Whether to re-raise the exception
            
        Returns:
            Function result or default_return on error
        """
        try:
            return func()
        except Exception as e:
            print(f"Error: {error_message}: {e}")
            if raise_exception:
                raise
            return default_return


class DataProcessor:
    """Common data processing utilities"""
    
    @staticmethod
    def validate_data_keys(data: Dict, required_keys: list, context: str = "data") -> bool:
        """
        Validate that required keys exist in data dictionary
        
        Args:
            data: Dictionary to validate
            required_keys: List of required key names
            context: Context description for error messages
            
        Returns:
            True if all keys present, False otherwise
        """
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            print(f"Error: {context} missing required keys: {', '.join(missing_keys)}")
            return False
        return True
    
    @staticmethod
    def safe_numeric_conversion(value: Any, default: float = 0.0) -> float:
        """
        Safely convert value to float with default fallback
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            Float value or default
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return default


class ConfigManager:
    """Manage common configuration settings"""
    
    # Default directories
    DATA_DIR = "data"
    REPORTS_DIR = "reports"
    MODELS_DIR = "models"
    
    # Common file patterns
    PYTHON_EXTENSIONS = ['.py']
    DATA_EXTENSIONS = ['.csv', '.json', '.xlsx']
    
    @classmethod
    def get_data_dir(cls) -> Path:
        """Get data directory path, create if doesn't exist"""
        return FileUtils.ensure_dir_exists(cls.DATA_DIR)
    
    @classmethod
    def get_reports_dir(cls) -> Path:
        """Get reports directory path, create if doesn't exist"""
        return FileUtils.ensure_dir_exists(cls.REPORTS_DIR)
    
    @classmethod
    def get_models_dir(cls) -> Path:
        """Get models directory path, create if doesn't exist"""
        return FileUtils.ensure_dir_exists(cls.MODELS_DIR)


def print_section_header(title: str, width: int = 70, char: str = "=") -> None:
    """
    Print a formatted section header
    
    Args:
        title: Header title
        width: Total width of header
        char: Character to use for border
    """
    print("\n" + char * width)
    print(title.center(width))
    print(char * width + "\n")


def print_success(message: str) -> None:
    """Print a success message with checkmark"""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message with X mark"""
    print(f"✗ {message}")


def print_warning(message: str) -> None:
    """Print a warning message"""
    print(f"⚠️  {message}")


def print_info(message: str) -> None:
    """Print an info message"""
    print(f"ℹ️  {message}")
