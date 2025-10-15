# 🤖 RizBot - Chatbot Predictive Maintenance (PdM)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/RF-AI-PDM/rizbot)

Chatbot ini dirancang untuk **Predictive Maintenance (PdM)** dengan dukungan analisis data dari dokumen teknik (PDF, CSV, dsb.).  
Tujuan project ini: membantu teknisi memahami data vibrasi, MCSA, DGA, dan membuat rekomendasi perawatan.

## ✨ Fitur

- 🔍 **Analisis Vibrasi** - Deteksi unbalance, misalignment, bearing fault
- ⚡ **MCSA** - Motor Current Signature Analysis
- 🧪 **DGA** - Dissolved Gas Analysis untuk transformer
- 🔧 **Rekomendasi Maintenance** - Saran perawatan berdasarkan kondisi
- 💬 **Chatbot CLI** - Interface interaktif untuk bertanya dan mendapat jawaban

## 📂 Struktur Folder

```
rizbot/
├── data/              # Dataset & dokumen (PDF, CSV, dll.)
│   └── IEEE-dga.csv   # Data standar DGA untuk transformer
├── intents.json       # Daftar intent & jawaban chatbot
├── chatbot.py         # Main script chatbot CLI
├── example.py         # Script demo penggunaan RizBot
├── requirements.txt   # Daftar dependencies Python
├── .gitignore         # File yang diabaikan Git
├── LICENSE            # MIT License
└── README.md          # Dokumentasi project
```

## 🚀 Instalasi

### Prerequisites
- Python 3.10 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/RF-AI-PDM/rizbot.git
cd rizbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan chatbot:
```bash
python chatbot.py
```

## 💻 Cara Penggunaan

### Mode Interaktif (CLI)

Setelah menjalankan `python chatbot.py`, Anda akan disambut dengan interface RizBot:

```
======================================================================
🤖 RizBot - Chatbot Predictive Maintenance (PdM)
======================================================================

Selamat datang! Saya RizBot, assistant untuk Predictive Maintenance.
Saya dapat membantu Anda dengan:
  • Analisis Vibrasi
  • Motor Current Signature Analysis (MCSA)
  • Dissolved Gas Analysis (DGA)
  • Rekomendasi Maintenance

Ketik 'quit' atau 'exit' untuk keluar.
Ketik 'help' untuk melihat daftar topik.
----------------------------------------------------------------------

Anda: 
```

### Mode Programmatic

Anda juga dapat menggunakan RizBot dalam script Python Anda:

```python
from chatbot import RizBot

# Initialize chatbot
bot = RizBot('intents.json')

# Get response
response, confidence = bot.get_response("Apa itu analisis vibrasi?")
print(response)
```

Atau jalankan contoh demo:
```bash
python example.py
```

### Contoh Pertanyaan

- "Apa itu analisis vibrasi?"
- "Jelaskan tentang MCSA"
- "Bagaimana cara menganalisis DGA?"
- "Apa itu bearing fault?"
- "Rekomendasi perawatan untuk vibrasi tinggi"
- "Jelaskan tentang misalignment"
- "Help" (untuk melihat daftar topik)

### Keluar dari Chatbot

Ketik salah satu dari: `quit`, `exit`, `bye`, atau `goodbye`

## 🎯 Topik yang Didukung

1. **Vibration Analysis** - Analisis getaran mesin untuk deteksi dini kerusakan
2. **MCSA** - Analisis arus motor untuk identifikasi fault
3. **DGA** - Analisis gas terlarut dalam minyak transformer
4. **Bearing Fault** - Deteksi kerusakan bearing
5. **Misalignment** - Deteksi ketidakselarasan shaft
6. **Unbalance** - Deteksi ketidakseimbangan rotor
7. **Maintenance Recommendations** - Rekomendasi perawatan

## 🔧 Dependencies

- `numpy` - Numerical computing
- `nltk` - Natural Language Toolkit untuk NLP
- `scikit-learn` - Machine learning untuk text similarity
- `pandas` - Data analysis (untuk analisis CSV)

## 📊 Dataset

Repository ini menyertakan dataset:
- **IEEE-dga.csv** - Standar IEEE untuk interpretasi Dissolved Gas Analysis pada transformer

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:
1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👥 Authors

- **RF-AI-PDM** - *Initial work* - [RF-AI-PDM](https://github.com/RF-AI-PDM)

## 🙏 Acknowledgments

- Dataset DGA berdasarkan standar IEEE
- Natural Language Processing menggunakan NLTK
- Machine Learning dengan scikit-learn

---

Made with ❤️ by RF-AI-PDM Team


