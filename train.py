"""
Training Script untuk RizBot PdM Deep Learning Chatbot
Script terpisah untuk training model tanpa interface chat
"""

import os
import sys
import matplotlib.pyplot as plt
from src.deep_learning_chatbot import PdMChatbot, train_new_model

def plot_training_history(history):
    """
    Plot training history untuk analisis performa model
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot training loss
    ax1.plot(history.history['loss'])
    ax1.set_title('Model Loss')
    ax1.set_ylabel('Loss')
    ax1.set_xlabel('Epoch')
    ax1.grid(True)
    
    # Plot training accuracy
    ax2.plot(history.history['accuracy'])
    ax2.set_title('Model Accuracy')
    ax2.set_ylabel('Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("📊 Training history plot disimpan ke 'models/training_history.png'")

def evaluate_model(chatbot):
    """
    Evaluasi model dengan test cases
    """
    print("\n=== 🧪 EVALUASI MODEL ===")
    
    test_cases = [
        "Hello",
        "Bagaimana analisis vibrasi?",
        "MCSA motor rusak",
        "DGA transformer",
        "Maintenance recommendation",
        "Help me",
        "Bye"
    ]
    
    print(f"{'Input':<30} {'Intent':<20} {'Confidence':<12} {'Response'}")
    print("-" * 100)
    
    for test in test_cases:
        response, intent, confidence = chatbot.predict_response(test)
        intent_str = intent if intent else "unknown"
        conf_str = f"{confidence:.3f}" if confidence else "0.000"
        response_short = response[:50] + "..." if len(response) > 50 else response
        
        print(f"{test:<30} {intent_str:<20} {conf_str:<12} {response_short}")

def advanced_training():
    """
    Training dengan monitoring dan evaluasi lengkap
    """
    print("=== 🚀 ADVANCED TRAINING RIZBOT ===\n")
    
    # Pastikan direktori ada
    os.makedirs('models', exist_ok=True)
    
    # Inisialisasi chatbot
    chatbot = PdMChatbot()
    
    # Preprocessing
    print("Step 1: Preprocessing data...")
    chatbot.preprocess_data()
    
    # Buat training data
    print("\nStep 2: Membuat training data...")
    chatbot.create_training_data()
    
    # Build model
    print("\nStep 3: Membangun Neural Network...")
    chatbot.build_model()
    
    # Print model summary
    print("\nModel Architecture:")
    chatbot.model.summary()
    
    # Training dengan history tracking
    print("\nStep 4: Training model...")
    history = chatbot.train_model(epochs=300, batch_size=8, verbose=1)
    
    # Plot training history
    print("\nStep 5: Visualisasi training...")
    plot_training_history(history)
    
    # Simpan model
    print("\nStep 6: Menyimpan model...")
    chatbot.save_model()
    
    # Evaluasi model
    print("\nStep 7: Evaluasi model...")
    evaluate_model(chatbot)
    
    print("\n✅ Advanced training selesai!")
    return chatbot

def quick_test():
    """
    Quick test untuk model yang sudah ada
    """
    print("=== 🧪 QUICK TEST MODEL ===\n")
    
    chatbot = PdMChatbot()
    
    if not chatbot.load_model():
        print("❌ Model tidak ditemukan. Jalankan training dulu!")
        return
    
    print("✅ Model berhasil dimuat!")
    evaluate_model(chatbot)

def main():
    """
    Main function dengan pilihan menu
    """
    print("🤖 RizBot Training Manager")
    print("=" * 40)
    print("1. Advanced Training (Full)")
    print("2. Quick Training (Basic)")  
    print("3. Test Model")
    print("4. Exit")
    
    choice = input("\nPilih opsi (1-4): ").strip()
    
    if choice == "1":
        advanced_training()
    elif choice == "2":
        train_new_model()
    elif choice == "3":
        quick_test()
    elif choice == "4":
        print("Goodbye! 👋")
    else:
        print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()