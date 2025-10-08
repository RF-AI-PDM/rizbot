#!/usr/bin/env python3
"""
Simple demo script to show how intents.json can be used for DGA chatbot
"""
import json
import random
import os
from pathlib import Path
from difflib import get_close_matches

def load_intents(filename):
    """Load intents from JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['intents']

def find_intent(user_input, intents):
    """Find the best matching intent based on user input"""
    user_input_lower = user_input.lower()
    
    # Check for exact pattern matches first
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input_lower or user_input_lower in pattern.lower():
                return intent
    
    # If no exact match, try fuzzy matching
    all_patterns = []
    pattern_to_intent = {}
    
    for intent in intents:
        for pattern in intent['patterns']:
            all_patterns.append(pattern.lower())
            pattern_to_intent[pattern.lower()] = intent
    
    matches = get_close_matches(user_input_lower, all_patterns, n=1, cutoff=0.4)
    if matches:
        return pattern_to_intent[matches[0]]
    
    return None

def demo_chatbot():
    """Demo the DGA chatbot functionality"""
    print("=== DGA Chatbot Demo ===")
    print("Loading intents.json...")
    
    # Use relative path or path relative to script location
    script_dir = Path(__file__).parent
    intents_file = script_dir / 'intents.json'
    
    intents = load_intents(intents_file)
    print(f"Loaded {len(intents)} intent categories")
    
    # Display available topics
    print("\nAvailable topics:")
    for intent in intents:
        if intent['tag'] not in ['greeting', 'goodbye']:
            print(f"  - {intent['tag'].replace('_', ' ').title()}")
    
    print("\n" + "="*50)
    print("Try asking questions like:")
    print("- 'What is DGA?'")
    print("- 'Tell me about acetylene'")
    print("- 'How do I interpret DGA results?'")
    print("- 'What are thermal faults?'")
    print("- 'goodbye' to exit")
    print("="*50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("Bot: Thank you for using the DGA assistant! Stay safe with your transformer maintenance. Goodbye!")
                break
            
            # Find matching intent
            matched_intent = find_intent(user_input, intents)
            
            if matched_intent:
                response = random.choice(matched_intent['responses'])
                print(f"Bot: {response}")
            else:
                print("Bot: I'm not sure how to help with that specific question. Try asking about DGA basics, gas analysis, fault types, or interpretation methods.")
                
        except KeyboardInterrupt:
            print("\nBot: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    demo_chatbot()