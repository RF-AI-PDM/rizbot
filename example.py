#!/usr/bin/env python3
"""
Example script demonstrating RizBot usage
"""

import sys
import os

# Import RizBot class
from chatbot import RizBot

def main():
    """Example usage of RizBot"""
    print("=" * 70)
    print("RizBot Example - Automated Q&A Demo")
    print("=" * 70)
    print()
    
    # Initialize chatbot
    bot = RizBot('intents.json')
    
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

if __name__ == "__main__":
    main()
