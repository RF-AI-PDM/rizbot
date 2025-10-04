#!/usr/bin/env python3
"""
Example script demonstrating how to use ChatbotPdM programmatically
"""

from chatbot import ChatbotPdM


def test_chatbot():
    """Test chatbot with various queries"""
    print("=" * 70)
    print("Testing Chatbot PdM")
    print("=" * 70)
    
    # Initialize chatbot
    bot = ChatbotPdM("intents.json")
    
    # Test queries
    test_queries = [
        "halo",
        "apa itu DGA?",
        "jelaskan analisis vibrasi",
        "MCSA untuk motor",
        "bearing failure detection",
        "help",
        "random query that doesn't match",
        "thank you"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "=" * 70)
    print("Testing completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_chatbot()
