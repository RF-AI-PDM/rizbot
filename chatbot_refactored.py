#!/usr/bin/env python3
"""
RizBot - Chatbot Predictive Maintenance (PdM)
Author: RF-AI-PDM
Description: Chatbot CLI untuk membantu analisis vibrasi, MCSA, DGA dan rekomendasi maintenance

REFACTORED VERSION: Uses common_utils for shared functionality
"""

import random
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import common utilities (eliminates duplicated code)
from common_utils import (
    FileUtils, ErrorHandler, print_section_header, 
    print_success, print_error, print_warning
)


# Download NLTK data if not available
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt_tab', quiet=True)


class RizBot:
    """Chatbot for Predictive Maintenance assistance"""
    
    def __init__(self, intents_file='intents.json'):
        """
        Initialize RizBot dengan intents file
        
        Args:
            intents_file: Path to intents JSON file
        """
        self.stemmer = PorterStemmer()
        # Use common FileUtils instead of custom load_intents
        self.intents = FileUtils.load_json(intents_file, "intents")
        self.vectorizer = TfidfVectorizer(tokenizer=self.tokenize)
        self.prepare_training_data()
        
    def tokenize(self, text):
        """
        Tokenize and stem text
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of stemmed tokens
        """
        tokens = nltk.word_tokenize(text.lower())
        return [self.stemmer.stem(token) for token in tokens if token.isalnum()]
    
    def prepare_training_data(self):
        """Prepare training data from intents"""
        self.patterns = []
        self.tags = []
        self.responses = {}
        
        for intent in self.intents['intents']:
            tag = intent['tag']
            self.responses[tag] = intent['responses']
            
            for pattern in intent['patterns']:
                self.patterns.append(pattern)
                self.tags.append(tag)
        
        # Fit vectorizer with all patterns
        self.pattern_vectors = self.vectorizer.fit_transform(self.patterns)
        print_success(f"Prepared {len(self.patterns)} patterns from {len(self.responses)} intents")
    
    def get_response(self, user_input):
        """
        Get response based on user input
        
        Args:
            user_input: User's question or statement
            
        Returns:
            Tuple of (response_text, confidence_score)
        """
        # Vectorize user input
        user_vector = self.vectorizer.transform([user_input])
        
        # Calculate similarity with all patterns
        similarities = cosine_similarity(user_vector, self.pattern_vectors).flatten()
        
        # Get index with highest similarity
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Threshold for confidence
        if best_similarity > 0.3:
            tag = self.tags[best_match_idx]
            response = random.choice(self.responses[tag])
            return response, best_similarity
        else:
            default_response = (
                "Maaf, saya tidak mengerti pertanyaan Anda. "
                "Coba tanyakan tentang vibrasi, MCSA, DGA, atau maintenance. "
                "Ketik 'help' untuk melihat topik yang tersedia."
            )
            return default_response, 0.0
    
    def run(self):
        """Run chatbot CLI interface"""
        print_section_header("🤖 RizBot - Chatbot Predictive Maintenance (PdM)")
        
        print("Selamat datang! Saya RizBot, assistant untuk Predictive Maintenance.")
        print("Saya dapat membantu Anda dengan:")
        print("  • Analisis Vibrasi")
        print("  • Motor Current Signature Analysis (MCSA)")
        print("  • Dissolved Gas Analysis (DGA)")
        print("  • Rekomendasi Maintenance")
        print("\nKetik 'quit' atau 'exit' untuk keluar.")
        print("Ketik 'help' untuk melihat daftar topik.")
        print("-" * 70 + "\n")
        
        while True:
            try:
                user_input = input("Anda: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\nRizBot: Terima kasih telah menggunakan RizBot! Sampai jumpa! 👋\n")
                    break
                
                # Get response from chatbot
                response, confidence = self.get_response(user_input)
                
                print(f"\nRizBot: {response}")
                
                # Show confidence indicator (for debugging/transparency)
                if confidence > 0.0:
                    confidence_emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.5 else "🟠"
                    # Uncomment to show confidence score:
                    # print(f"[Confidence: {confidence_emoji} {confidence:.2f}]")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nRizBot: Terima kasih! Sampai jumpa! 👋\n")
                break
            except Exception as e:
                print_error(f"Unexpected error: {e}")
                continue


def main():
    """Main function"""
    # Check if intents.json exists
    if not FileUtils.check_file_exists('intents.json', "Intents file"):
        print("Pastikan file intents.json ada di direktori yang sama dengan chatbot.py")
        return 1
    
    # Initialize and run chatbot with error handling
    def run_bot():
        bot = RizBot('intents.json')
        bot.run()
        return 0
    
    return ErrorHandler.safe_execute(
        run_bot,
        error_message="Failed to run chatbot",
        default_return=1
    )


if __name__ == "__main__":
    exit(main())
