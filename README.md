# rizbot
membangun chatbot Predictive Maintenance (PdM) yang mampu:
# 🤖 Chatbot PdM (Predictive Maintenance)

![GitHub Repo stars](https://img.shields.io/github/stars/username/chatbot-pdm?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/chatbot-pdm?style=social)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/username/chatbot-pdm)
![Last Commit](https://img.shields.io/github/last-commit/username/chatbot-pdm)

Chatbot ini dirancang untuk **Predictive Maintenance (PdM)** dengan dukungan analisis data dari dokumen teknik (PDF, CSV, dsb.).  
Tujuan project ini: membantu teknisi memahami data vibrasi, MCSA, DGA, dan membuat rekomendasi perawatan.

---

## 📂 Struktur Folder
```
chatbot-pdm/
│── data/                    # Dataset & dokumen (PDF, CSV, dll.)
│── intents.json             # Daftar intent & jawaban chatbot
│── demo_chatbot.py          # Demo script chatbot CLI
│── config_search.py         # Tool untuk mencari konfigurasi
│── CONFIG_SEARCH_README.md  # Dokumentasi configuration search tool
│── README.md                # Dokumentasi project
```

## 🔍 Configuration Search Tool

Project ini dilengkapi dengan tool untuk mencari dan mengidentifikasi konfigurasi dalam kode:

```bash
python3 config_search.py
```

Tool ini akan mencari:
- File paths yang hardcoded
- Potensi API keys atau credentials
- Environment variables
- Pattern konfigurasi lainnya

Lihat [CONFIG_SEARCH_README.md](CONFIG_SEARCH_README.md) untuk detail lengkap.


