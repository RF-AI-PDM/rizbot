#!/usr/bin/env python3
"""
🤖 RizBot - Chatbot Predictive Maintenance (PdM)
Chatbot dengan Deep Learning untuk analisis dan rekomendasi maintenance

Author: RF-AI-PDM
License: MIT
"""

import os
import sys
import time
from colorama import init, Fore, Style
from src.deep_learning_chatbot import PdMChatbot, train_new_model

# Inisialisasi colorama untuk Windows compatibility
init()

def print_banner():
    """Tampilkan banner RizBot"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    🤖 RizBot PdM v1.0                        ║
║              Predictive Maintenance Assistant                ║
║                    Powered by Deep Learning                  ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Fitur RizBot:{Style.RESET_ALL}
• Analisis Vibrasi (Vibration Analysis)
• Motor Current Signature Analysis (MCSA) 
• Dissolved Gas Analysis (DGA)
• Rekomendasi Maintenance Strategy
• Learning dari conversational data

{Fore.GREEN}Ketik 'help' untuk bantuan, 'quit' untuk keluar{Style.RESET_ALL}
"""
    print(banner)

def print_response(message, intent=None, confidence=None):
    """Print response dengan formatting yang menarik"""
    print(f"\n{Fore.BLUE}🤖 RizBot:{Style.RESET_ALL} {message}")
    
    if intent and confidence:
        conf_color = Fore.GREEN if confidence > 0.8 else Fore.YELLOW if confidence > 0.5 else Fore.RED
        print(f"{Fore.LIGHTBLACK_EX}   └─ Intent: {intent} | Confidence: {conf_color}{confidence:.2f}{Style.RESET_ALL}")

def chat_interface():
    """Interface chat interaktif"""
    print_banner()
    
    # Load atau train model
    chatbot = PdMChatbot()
    
    if not os.path.exists('models/chatbot_model.h5'):
        print(f"\n{Fore.YELLOW}⚠️  Model belum tersedia. Memulai training...{Style.RESET_ALL}")
        print("Ini akan memakan waktu beberapa menit...")
        
        chatbot = train_new_model()
    else:
        print(f"\n{Fore.GREEN}📂 Loading model yang sudah ada...{Style.RESET_ALL}")
        if not chatbot.load_model():
            print(f"{Fore.RED}❌ Gagal load model. Memulai training ulang...{Style.RESET_ALL}")
            chatbot = train_new_model()
    
    print(f"\n{Fore.GREEN}✅ RizBot siap membantu analisis PdM Anda!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}────────────────────────────────────────────────────────{Style.RESET_ALL}")
    
    # Main chat loop
    while True:
        try:
            # Input dari user
            user_input = input(f"\n{Fore.GREEN}👤 Anda:{Style.RESET_ALL} ").strip()
            
            if not user_input:
                continue
                
            # Command untuk keluar
            if user_input.lower() in ['quit', 'exit', 'bye', 'keluar']:
                print(f"\n{Fore.BLUE}🤖 RizBot:{Style.RESET_ALL} Terima kasih! Jaga peralatan dengan baik! 👋")
                break
            
            # Command untuk help
            if user_input.lower() in ['help', 'bantuan']:
                show_help()
                continue
            
            # Command untuk retrain
            if user_input.lower() in ['retrain', 'train', 'latih']:
                print(f"\n{Fore.YELLOW}🔄 Memulai training ulang...{Style.RESET_ALL}")
                chatbot = train_new_model()
                print(f"{Fore.GREEN}✅ Training selesai! Model telah diperbarui.{Style.RESET_ALL}")
                continue
            
            # Prediksi response
            start_time = time.time()
            response, intent, confidence = chatbot.predict_response(user_input)
            processing_time = time.time() - start_time
            
            # Tampilkan response
            print_response(response, intent, confidence)
            print(f"{Fore.LIGHTBLACK_EX}   └─ Response time: {processing_time:.3f}s{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.BLUE}🤖 RizBot:{Style.RESET_ALL} Sampai jumpa! Tetap jaga kondisi equipment! 👋")
            break
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Coba restart RizBot atau ketik 'help' untuk bantuan{Style.RESET_ALL}")

def show_help():
    """Tampilkan help menu"""
    help_text = f"""
{Fore.CYAN}═══════════════ 📖 RizBot Help Menu ═══════════════{Style.RESET_ALL}

{Fore.YELLOW}🔧 Topik yang Bisa Ditanyakan:{Style.RESET_ALL}
• {Fore.GREEN}Vibration Analysis{Style.RESET_ALL} - Analisis getaran mesin
• {Fore.GREEN}MCSA{Style.RESET_ALL} - Motor Current Signature Analysis  
• {Fore.GREEN}DGA{Style.RESET_ALL} - Dissolved Gas Analysis
• {Fore.GREEN}Maintenance Recommendations{Style.RESET_ALL} - Rekomendasi perawatan
• {Fore.GREEN}Equipment Diagnosis{Style.RESET_ALL} - Diagnosis kerusakan

{Fore.YELLOW}📝 Contoh Pertanyaan:{Style.RESET_ALL}
• "Bagaimana cara analisis vibrasi bearing?"
• "Jelaskan tentang MCSA untuk motor 3 phase"
• "Interpretasi hasil DGA transformer"
• "Kapan harus maintenance preventif?"
• "Rekomendasi untuk getaran tinggi"

{Fore.YELLOW}⚙️  Command Khusus:{Style.RESET_ALL}
• {Fore.CYAN}help{Style.RESET_ALL} - Tampilkan menu bantuan
• {Fore.CYAN}retrain{Style.RESET_ALL} - Training ulang model
• {Fore.CYAN}quit{Style.RESET_ALL} - Keluar dari aplikasi

{Fore.GREEN}💡 Tip:{Style.RESET_ALL} Gunakan bahasa Indonesia atau Inggris. Semakin spesifik pertanyaan, semakin akurat jawaban!
"""
    print(help_text)

def main():
    """Main function"""
    try:
        # Pastikan direktori models ada
        os.makedirs('models', exist_ok=True)
        
        # Jalankan chat interface
        chat_interface()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()