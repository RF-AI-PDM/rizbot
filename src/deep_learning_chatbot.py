"""
Deep Learning Chatbot for Predictive Maintenance (PdM)
Menggunakan Neural Network untuk intent classification dan response generation
"""

import json
import numpy as np
import pandas as pd
import pickle
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding
from tensorflow.keras.optimizers import SGD, Adam
import warnings
warnings.filterwarnings("ignore")

class PdMChatbot:
    def __init__(self, intents_file='data/intents.json'):
        """
        Initialize Predictive Maintenance Chatbot dengan Deep Learning
        """
        self.intents_file = intents_file
        self.lemmatizer = WordNetLemmatizer()
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '.', ',', '!']
        self.model = None
        self.label_encoder = LabelEncoder()
        
        # Download NLTK data jika belum ada
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        # Load intents
        self.load_intents()
    
    def load_intents(self):
        """Load intents dari file JSON"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                self.intents = json.load(f)
        except FileNotFoundError:
            print(f"File {self.intents_file} tidak ditemukan!")
            self.intents = {"intents": []}
    
    def preprocess_data(self):
        """
        Preprocessing data untuk training:
        - Tokenisasi
        - Lemmatization
        - Bag of Words creation
        """
        print("🔄 Preprocessing data training...")
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Tokenisasi setiap kata
                w = word_tokenize(pattern.lower())
                self.words.extend(w)
                
                # Tambah ke documents
                self.documents.append((w, intent['tag']))
                
                # Tambah ke classes jika belum ada
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        
        # Lemmatisasi dan hapus duplikasi
        self.words = [self.lemmatizer.lemmatize(w) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        
        # Sort classes
        self.classes = sorted(list(set(self.classes)))
        
        print(f"📊 Dokumen: {len(self.documents)}")
        print(f"📊 Classes: {len(self.classes)} - {self.classes}")
        print(f"📊 Unique words: {len(self.words)}")
    
    def create_training_data(self):
        """
        Membuat training data dalam format yang sesuai untuk neural network
        """
        print("🔄 Membuat training data...")
        
        training = []
        output_empty = [0] * len(self.classes)
        
        for doc in self.documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [self.lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            
            # Membuat bag of words
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)
            
            # Output adalah '1' untuk current tag dan '0' untuk yang lain
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            
            training.append([bag, output_row])
        
        # Shuffle training data
        random.shuffle(training)
        
        # Konversi ke numpy arrays
        self.train_x = np.array([item[0] for item in training], dtype=np.float32)
        self.train_y = np.array([item[1] for item in training], dtype=np.float32)
        
        print(f"✅ Training data dibuat: X{self.train_x.shape}, Y{self.train_y.shape}")
    
    def build_model(self):
        """
        Membangun Deep Neural Network untuk intent classification
        """
        print("🧠 Membangun Neural Network model...")
        
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.train_y[0]), activation='softmax'))
        
        # Compile model
        sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        
        self.model = model
        print("✅ Model berhasil dibangun!")
        return model
    
    def train_model(self, epochs=200, batch_size=5, verbose=1):
        """
        Training model dengan data yang sudah dipreprocess
        """
        print("🚀 Memulai training model...")
        
        if self.model is None:
            self.build_model()
        
        # Training
        hist = self.model.fit(self.train_x, self.train_y,
                             epochs=epochs,
                             batch_size=batch_size,
                             verbose=verbose)
        
        print("✅ Training selesai!")
        return hist
    
    def save_model(self, model_path='models/chatbot_model.h5'):
        """
        Simpan model dan data preprocessing
        """
        print("💾 Menyimpan model...")
        
        # Simpan model
        self.model.save(model_path)
        
        # Simpan words, classes, dan documents
        with open('models/words.pkl', 'wb') as f:
            pickle.dump(self.words, f)
        
        with open('models/classes.pkl', 'wb') as f:
            pickle.dump(self.classes, f)
        
        with open('models/documents.pkl', 'wb') as f:
            pickle.dump(self.documents, f)
        
        print("✅ Model dan data berhasil disimpan!")
    
    def load_model(self, model_path='models/chatbot_model.h5'):
        """
        Load model dan data preprocessing yang sudah disimpan
        """
        try:
            print("📂 Loading model...")
            
            # Load model
            self.model = load_model(model_path)
            
            # Load words, classes, dan documents
            with open('models/words.pkl', 'rb') as f:
                self.words = pickle.load(f)
            
            with open('models/classes.pkl', 'rb') as f:
                self.classes = pickle.load(f)
            
            with open('models/documents.pkl', 'rb') as f:
                self.documents = pickle.load(f)
            
            print("✅ Model berhasil dimuat!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def clean_up_sentence(self, sentence):
        """
        Preprocessing input sentence
        """
        sentence_words = word_tokenize(sentence.lower())
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words
    
    def bag_of_words(self, sentence):
        """
        Konversi sentence ke bag of words format
        """
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
        
        return np.array(bag)
    
    def classify_intent(self, sentence, threshold=0.25):
        """
        Klasifikasi intent dari input sentence
        """
        if self.model is None:
            return None, 0
        
        # Generate bag of words
        p = self.bag_of_words(sentence)
        
        # Prediksi
        res = self.model.predict(np.array([p]), verbose=0)[0]
        
        # Filter predictions dengan threshold
        results = [[i, r] for i, r in enumerate(res) if r > threshold]
        
        # Sort by probability
        results.sort(key=lambda x: x[1], reverse=True)
        
        if results:
            return self.classes[results[0][0]], results[0][1]
        else:
            return None, 0
    
    def get_response(self, intent_tag):
        """
        Dapatkan response berdasarkan intent tag
        """
        for intent in self.intents['intents']:
            if intent['tag'] == intent_tag:
                return random.choice(intent['responses'])
        return "Maaf, saya tidak mengerti. Bisa dijelaskan lebih detail?"
    
    def predict_response(self, message):
        """
        Prediksi response lengkap dari input message
        """
        intent, confidence = self.classify_intent(message)
        
        if intent and confidence > 0.5:
            response = self.get_response(intent)
            return response, intent, confidence
        else:
            return "Maaf, saya kurang yakin dengan maksud Anda. Bisa coba dengan kata yang berbeda?", "unknown", confidence


def train_new_model():
    """
    Function untuk training model baru dari awal
    """
    print("=== 🚀 TRAINING CHATBOT PdM ===\n")
    
    # Inisialisasi chatbot
    bot = PdMChatbot()
    
    # Preprocessing
    bot.preprocess_data()
    
    # Buat training data
    bot.create_training_data()
    
    # Build dan train model
    bot.build_model()
    hist = bot.train_model(epochs=200, batch_size=5)
    
    # Simpan model
    bot.save_model()
    
    print("\n✅ Training selesai! Model siap digunakan.")
    return bot


if __name__ == "__main__":
    # Training model baru
    chatbot = train_new_model()