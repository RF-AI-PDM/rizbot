#!/usr/bin/env python3
"""
Example script demonstrating RizBot usage

REFACTORED VERSION: Uses common_utils for shared functionality
"""

# Import refactored chatbot
from chatbot_refactored import RizBot
from common_utils import print_section_header, ErrorHandler, FileUtils

# Configuration constants
INTENTS_FILE = 'intents.json'


def main():
    """Example usage of RizBot"""
    print_section_header("RizBot Example - Automated Q&A Demo")
    
    # Initialize chatbot with error handling
    def init_bot():
        if not FileUtils.check_file_exists(INTENTS_FILE, "Intents file"):
            raise FileNotFoundError(f"{INTENTS_FILE} not found")
        return RizBot(INTENTS_FILE)
    
    bot = ErrorHandler.safe_execute(
        init_bot,
        error_message="Could not initialize RizBot",
        default_return=None
    )
    
    if bot is None:
        print(f"Error: Make sure {INTENTS_FILE} exists in the current directory.")
        return 1
    
    # List of example questions
    questions = [
        "Hello",
        "What is vibration analysis?",
        "Explain MCSA",
        "Tell me about DGA",
        "What are bearing faults?",
        "Maintenance recommendations",
        "Thank you"
    ]
    
    # Ask each question
    for question in questions:
        print(f"Question: {question}")
        response, confidence = bot.get_response(question)
        print(f"RizBot: {response}")
        print(f"(Confidence: {confidence:.2f})")
        print("-" * 70)
        print()
    
    print("Demo complete!")
    return 0


if __name__ == "__main__":
    exit(main())
