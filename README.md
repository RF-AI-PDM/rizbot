# 🤖 RizBot - Chatbot PdM (Predictive Maintenance)

![GitHub Repo stars](https://img.shields.io/github/stars/RF-AI-PDM/rizbot?style=social)
![GitHub forks](https://img.shields.io/github/forks/RF-AI-PDM/rizbot?style=social)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/RF-AI-PDM/rizbot)
![Last Commit](https://img.shields.io/github/last-commit/RF-AI-PDM/rizbot)

Chatbot berbasis AI untuk **Predictive Maintenance (PdM)** yang dirancang untuk membantu teknisi dan engineer dalam memahami dan menganalisis data maintenance dari berbagai sumber teknik.

## 🎯 Tujuan Project

Membangun chatbot yang mampu:
- ✅ Menjawab pertanyaan tentang **DGA (Dissolved Gas Analysis)** untuk transformer
- ✅ Menjelaskan **Vibration Analysis** untuk rotating equipment
- ✅ Membantu analisis **MCSA (Motor Current Signature Analysis)**
- ✅ Memberikan panduan **Bearing Fault Detection**
- ✅ Menjelaskan konsep **Predictive Maintenance** dan **CBM**
- 🔄 Menganalisis data dari dokumen teknik (PDF, CSV) - *dalam pengembangan*

---

## 📂 Struktur Folder

```
rizbot/
├── data/                    # Dataset & dokumen teknik
│   └── IEEE-dga.csv        # Dataset DGA IEEE C57.104
├── intents.json            # Daftar intent & responses chatbot
├── chatbot.py              # Main script chatbot CLI
├── requirements.txt        # Dependencies Python
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── CODE_OF_CONDUCT        # Code of conduct
└── README.md              # Dokumentasi project
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/RF-AI-PDM/rizbot.git
cd rizbot
```

### 2. Install Dependencies

```bash
# Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

### 3. Jalankan Chatbot

```bash
python chatbot.py
```

### 4. Mulai Chat!

```
🤖 Chatbot PdM (Predictive Maintenance)
======================================================================
Selamat datang! Saya siap membantu Anda dengan analisis PdM.
Topik: DGA, Vibration, MCSA, Bearing Analysis, Oil Analysis, dll.
Ketik 'quit', 'exit', atau 'bye' untuk keluar.
======================================================================

Anda: Apa itu DGA?
Bot: DGA (Dissolved Gas Analysis) adalah metode untuk menganalisis gas terlarut...
```

---

## 💡 Fitur Utama

### 1. **DGA (Dissolved Gas Analysis)**
- Penjelasan metode DGA untuk transformer
- Interpretasi gas H2, CH4, C2H2, C2H4, C2H6, CO, CO2
- Metode Roger Ratio, Duval Triangle, IEEE C57.104

### 2. **Vibration Analysis**
- Analisis getaran mesin
- FFT (Fast Fourier Transform) analysis
- Deteksi unbalance, misalignment, looseness

### 3. **MCSA (Motor Current Signature Analysis)**
- Analisis arus motor
- Deteksi broken rotor bars
- Bearing fault detection via current signature

### 4. **Bearing Fault Detection**
- Frekuensi karakteristik: BPFO, BPFI, BSF, FTF
- Envelope analysis
- Root cause analysis

### 5. **Temperature & Oil Monitoring**
- Thermal imaging
- Hotspot detection
- Oil condition monitoring

---

## 📚 Contoh Penggunaan

### Pertanyaan Umum PdM:
```
Anda: Apa itu predictive maintenance?
Anda: Jelaskan analisis vibrasi
Anda: Bagaimana cara interpretasi DGA?
```

### Troubleshooting:
```
Anda: Bearing failure detection
Anda: BPFO frequency
Anda: Roger ratio method
```

### Bantuan:
```
Anda: help
Anda: bantuan
Anda: apa yang bisa kamu lakukan?
```

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.10+** - Bahasa pemrograman utama
- **JSON** - Format data untuk intents
- **Pattern Matching** - Untuk intent classification
- **Pandas & NumPy** - Data processing (untuk fitur mendatang)
- **NLTK** - Natural Language Processing (untuk fitur mendatang)

---

## 📈 Roadmap

- [x] Implementasi chatbot CLI dasar
- [x] Intent-based response system
- [x] Dokumentasi lengkap
- [ ] Integrasi dengan data CSV (DGA analysis)
- [ ] Machine Learning untuk intent classification
- [ ] Web interface dengan Streamlit/Flask
- [ ] PDF document analysis
- [ ] Multi-language support (English)
- [ ] Export chat history
- [ ] Integration dengan IoT sensors

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

## 📝 License

Project ini menggunakan MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

## 👥 Authors

**RF-AI-PDM Team**
- GitHub: [@RF-AI-PDM](https://github.com/RF-AI-PDM)

---

## 🙏 Acknowledgments

- IEEE C57.104 Standard untuk DGA interpretation
- Komunitas Predictive Maintenance Indonesia
- Open source contributors

---

## 📧 Kontak

Untuk pertanyaan atau saran, silakan buat [Issue](https://github.com/RF-AI-PDM/rizbot/issues) di repository ini.

---

**⭐ Jika project ini bermanfaat, jangan lupa berikan star!**

