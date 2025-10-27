#!/usr/bin/env python3
"""
Chatbot PdM (Predictive Maintenance)
A chatbot for Predictive Maintenance assistance with DGA, Vibration, MCSA analysis
"""

import json
import random
import re
from typing import List, Dict, Tuple
import os


class ChatbotPdM:
    """Predictive Maintenance Chatbot"""
    
    def __init__(self, intents_file: str = "intents.json"):
        """Initialize chatbot with intents file"""
        self.intents_file = intents_file
        self.intents = self._load_intents()
        
    def _load_intents(self) -> Dict:
        """Load intents from JSON file"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File {self.intents_file} tidak ditemukan!")
            return {"intents": []}
        except json.JSONDecodeError:
            print(f"Error: File {self.intents_file} tidak valid!")
            return {"intents": []}
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess user input text"""
        # Convert to lowercase and remove extra spaces
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _calculate_similarity(self, user_input: str, pattern: str) -> float:
        """Calculate similarity between user input and pattern"""
        user_input = self._preprocess_text(user_input)
        pattern = self._preprocess_text(pattern)
        
        # Simple word matching
        user_words = set(user_input.split())
        pattern_words = set(pattern.split())
        
        if not pattern_words:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = user_words.intersection(pattern_words)
        union = user_words.union(pattern_words)
        
        if not union:
            return 0.0
            
        similarity = len(intersection) / len(union)
        
        # Bonus for exact substring match
        if pattern in user_input or user_input in pattern:
            similarity += 0.3
            
        return min(similarity, 1.0)
    
    def _find_best_intent(self, user_input: str) -> Tuple[str, float]:
        """Find the best matching intent for user input"""
        best_intent = None
        best_score = 0.0
        
        for intent in self.intents.get("intents", []):
            for pattern in intent.get("patterns", []):
                score = self._calculate_similarity(user_input, pattern)
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        return best_intent, best_score
    
    def get_response(self, user_input: str, threshold: float = 0.3) -> str:
        """Get chatbot response for user input"""
        if not user_input.strip():
            return "Maaf, saya tidak mengerti. Bisa Anda ulangi?"
        
        intent, score = self._find_best_intent(user_input)
        
        if intent and score >= threshold:
            responses = intent.get("responses", [])
            if responses:
                return random.choice(responses)
        
        # Default response if no match found
        return ("Maaf, saya belum memahami pertanyaan Anda. "
                "Coba tanyakan tentang DGA, vibration analysis, MCSA, "
                "bearing failure, atau ketik 'help' untuk bantuan.")
    
    def chat(self):
        """Start interactive chat session"""
        print("=" * 70)
        print("🤖 Chatbot PdM (Predictive Maintenance)")
        print("=" * 70)
        print("Selamat datang! Saya siap membantu Anda dengan analisis PdM.")
        print("Topik: DGA, Vibration, MCSA, Bearing Analysis, Oil Analysis, dll.")
        print("Ketik 'quit', 'exit', atau 'bye' untuk keluar.")
        print("=" * 70)
        print()
        
        while True:
            try:
                user_input = input("Anda: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'keluar']:
                    print("\nBot: Terima kasih telah menggunakan Chatbot PdM. Sampai jumpa! 👋")
                    break
                
                response = self.get_response(user_input)
                print(f"\nBot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nBot: Terima kasih telah menggunakan Chatbot PdM. Sampai jumpa! 👋")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Terjadi kesalahan. Silakan coba lagi.\n")


def main():
    """Main function to run chatbot"""
    # Check if intents file exists
    intents_file = "intents.json"
    if not os.path.exists(intents_file):
        print(f"Error: File '{intents_file}' tidak ditemukan!")
        print("Pastikan file intents.json ada di direktori yang sama dengan chatbot.py")
        return
    
    # Initialize and run chatbot
    chatbot = ChatbotPdM(intents_file)
    chatbot.chat()


if __name__ == "__main__":
    main()
