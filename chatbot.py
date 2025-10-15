#!/usr/bin/env python3
"""
RizBot - Chatbot Predictive Maintenance (PdM)
Author: RF-AI-PDM
Description: Chatbot CLI untuk membantu analisis vibrasi, MCSA, DGA dan rekomendasi maintenance
"""

import json
import random
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

# Download NLTK data jika belum ada
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt_tab', quiet=True)

class RizBot:
    def __init__(self, intents_file='intents.json'):
        """Initialize RizBot dengan intents file"""
        self.stemmer = PorterStemmer()
        self.intents = self.load_intents(intents_file)
        self.vectorizer = TfidfVectorizer(tokenizer=self.tokenize)
        self.prepare_training_data()
        
    def load_intents(self, filename):
        """Load intents dari JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"✓ Loaded {len(data['intents'])} intents successfully")
            return data
        except FileNotFoundError:
            print(f"Error: File {filename} tidak ditemukan!")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Format JSON tidak valid di {filename}")
            sys.exit(1)
    
    def tokenize(self, text):
        """Tokenize dan stem text"""
        tokens = nltk.word_tokenize(text.lower())
        return [self.stemmer.stem(token) for token in tokens if token.isalnum()]
    
    def prepare_training_data(self):
        """Prepare training data dari intents"""
        self.patterns = []
        self.tags = []
        self.responses = {}
        
        for intent in self.intents['intents']:
            tag = intent['tag']
            self.responses[tag] = intent['responses']
            
            for pattern in intent['patterns']:
                self.patterns.append(pattern)
                self.tags.append(tag)
        
        # Fit vectorizer dengan semua patterns
        self.pattern_vectors = self.vectorizer.fit_transform(self.patterns)
    
    def get_response(self, user_input):
        """Get response berdasarkan user input"""
        # Vectorize user input
        user_vector = self.vectorizer.transform([user_input])
        
        # Hitung similarity dengan semua patterns
        similarities = cosine_similarity(user_vector, self.pattern_vectors).flatten()
        
        # Get index dengan similarity tertinggi
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Threshold untuk confidence
        if best_similarity > 0.3:
            tag = self.tags[best_match_idx]
            response = random.choice(self.responses[tag])
            return response, best_similarity
        else:
            return "Maaf, saya tidak mengerti pertanyaan Anda. Coba tanyakan tentang vibrasi, MCSA, DGA, atau maintenance. Ketik 'help' untuk melihat topik yang tersedia.", 0.0
    
    def run(self):
        """Run chatbot CLI"""
        print("\n" + "="*70)
        print("🤖 RizBot - Chatbot Predictive Maintenance (PdM)")
        print("="*70)
        print("\nSelamat datang! Saya RizBot, assistant untuk Predictive Maintenance.")
        print("Saya dapat membantu Anda dengan:")
        print("  • Analisis Vibrasi")
        print("  • Motor Current Signature Analysis (MCSA)")
        print("  • Dissolved Gas Analysis (DGA)")
        print("  • Rekomendasi Maintenance")
        print("\nKetik 'quit' atau 'exit' untuk keluar.")
        print("Ketik 'help' untuk melihat daftar topik.")
        print("-"*70 + "\n")
        
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
                
                # Show confidence if high enough (for debugging/transparency)
                if confidence > 0.0:
                    confidence_emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.5 else "🟠"
                    # print(f"[Confidence: {confidence_emoji} {confidence:.2f}]")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nRizBot: Terima kasih! Sampai jumpa! 👋\n")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue

def main():
    """Main function"""
    # Check if intents.json exists
    if not os.path.exists('intents.json'):
        print("Error: intents.json tidak ditemukan!")
        print("Pastikan file intents.json ada di direktori yang sama dengan chatbot.py")
        sys.exit(1)
    
    # Initialize and run chatbot
    bot = RizBot('intents.json')
    bot.run()

if __name__ == "__main__":
    main()
