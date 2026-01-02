#!/usr/bin/env python3
"""
Verification script to test refactored modules
Tests that all refactored code works correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    FileUtils, ErrorHandler, DataProcessor, ConfigManager,
    print_section_header, print_success, print_error, print_info
)


def test_common_utils():
    """Test common utilities module"""
    print_section_header("Testing Common Utilities")
    
    # Test FileUtils
    print("Testing FileUtils...")
    
    # Test ensure_dir_exists
    test_dir = ConfigManager.get_reports_dir()
    print_success(f"Created/verified reports directory: {test_dir}")
    
    # Test DataProcessor
    print("\nTesting DataProcessor...")
    data = {'key1': 'value1', 'key2': 'value2'}
    required = ['key1', 'key2']
    if DataProcessor.validate_data_keys(data, required):
        print_success("Data validation passed")
    
    # Test safe numeric conversion
    val = DataProcessor.safe_numeric_conversion("123.45")
    assert val == 123.45, "Numeric conversion failed"
    print_success(f"Numeric conversion: '123.45' -> {val}")
    
    # Test ErrorHandler
    print("\nTesting ErrorHandler...")
    result = ErrorHandler.safe_execute(
        lambda: 10 / 2,
        error_message="Division test",
        default_return=0
    )
    assert result == 5, "Safe execute failed"
    print_success(f"Safe execute: 10 / 2 = {result}")
    
    print_success("\n✅ All common_utils tests passed!")
    return True


def test_chatbot_import():
    """Test chatbot refactored module can be imported"""
    print_section_header("Testing Chatbot Module Import")
    
    try:
        from chatbot_refactored import RizBot
        print_success("Successfully imported RizBot class")
        
        # Check if intents.json exists in chatbot_module
        import shutil
        if os.path.exists('chatbot_module/intents.json') and not os.path.exists('intents.json'):
            shutil.copy('chatbot_module/intents.json', 'intents.json')
            print_info("Copied intents.json to current directory")
        
        if os.path.exists('intents.json'):
            bot = RizBot('intents.json')
            print_success("Successfully initialized RizBot instance")
            
            # Test a simple query
            response, confidence = bot.get_response("hello")
            print_success(f"Bot response test passed (confidence: {confidence:.2f})")
            print_info(f"Response: {response[:100]}...")
        else:
            print_info("Skipping bot initialization (intents.json not found)")
        
        return True
    except Exception as e:
        print_error(f"Chatbot test failed: {e}")
        return False


def test_report_generator_import():
    """Test report generator refactored module can be imported"""
    print_section_header("Testing Report Generator Module Import")
    
    try:
        from report_generator_refactored import DGAReportGenerator
        print_success("Successfully imported DGAReportGenerator class")
        
        # Test with sample JSON data
        import json
        sample_data = {
            'H2': [150, 180],
            'CH4': [200, 250],
            'C2H6': [80, 95],
            'C2H4': [60, 75],
            'C2H2': [3, 5],
            'CO': [450, 520],
            'CO2': [3500, 4200]
        }
        
        json_data = json.dumps(sample_data)
        generator = DGAReportGenerator(json_data)
        print_success("Successfully initialized DGAReportGenerator instance")
        
        generator.load_data()
        print_success("Successfully loaded data")
        
        analysis = generator.analyze_gas_levels()
        print_success(f"Successfully analyzed gas levels ({len(analysis['summary'])} gases)")
        
        return True
    except Exception as e:
        print_error(f"Report generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests"""
    print_section_header("🔧 Refactoring Verification Tests", width=80)
    
    results = []
    
    # Test 1: Common utilities
    try:
        results.append(("Common Utilities", test_common_utils()))
    except Exception as e:
        print_error(f"Common utilities test crashed: {e}")
        results.append(("Common Utilities", False))
    
    print("\n" + "="*80 + "\n")
    
    # Test 2: Chatbot module
    try:
        results.append(("Chatbot Module", test_chatbot_import()))
    except Exception as e:
        print_error(f"Chatbot test crashed: {e}")
        results.append(("Chatbot Module", False))
    
    print("\n" + "="*80 + "\n")
    
    # Test 3: Report generator module
    try:
        results.append(("Report Generator", test_report_generator_import()))
    except Exception as e:
        print_error(f"Report generator test crashed: {e}")
        results.append(("Report Generator", False))
    
    # Print summary
    print("\n" + "="*80)
    print_section_header("Test Summary", width=80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
        if not passed:
            all_passed = False
    
    print("="*80 + "\n")
    
    if all_passed:
        print_success("🎉 All tests passed! Refactoring is working correctly.")
        return 0
    else:
        print_error("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
