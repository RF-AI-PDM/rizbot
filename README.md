# 🤖 Rizbot - Predictive Maintenance (PdM)

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/github/license/RF-AI-PDM/rizbot)
![Last Commit](https://img.shields.io/github/last-commit/RF-AI-PDM/rizbot)

Chatbot dan tools untuk **Predictive Maintenance (PdM)** dengan dukungan analisis data dari dokumen teknik (PDF, CSV, dsb.).  
Tujuan project ini: membantu teknisi memahami data vibrasi, MCSA, DGA, dan membuat rekomendasi perawatan.

---

## ✨ Fitur Terbaru: DGA Report Generator

**Generator laporan otomatis untuk analisis DGA (Dissolved Gas Analysis)** - membuat laporan komprehensif dari data monitoring gas transformer dengan format Markdown dan HTML.

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate report dari CSV
python report_generator.py sample_data.csv

# Generate report dari data JSON
python example_usage.py
```

### 📊 Fitur Report Generator

✅ **Multiple Data Sources** - CSV files atau JSON data  
✅ **Analisis Otomatis** - Threshold checking berdasarkan IEEE C57.104  
✅ **Multiple Formats** - Markdown (.md) dan HTML (.html)  
✅ **Visualizations** - Charts dan graphs otomatis  
✅ **Actionable Recommendations** - Rekomendasi berdasarkan severity  

📖 **Dokumentasi lengkap:** Lihat [REPORT_GENERATOR_README.md](REPORT_GENERATOR_README.md)

---

## 📂 Struktur Project

```
rizbot/
├── report_generator.py        # Main report generator script
├── example_usage.py           # Contoh penggunaan
├── sample_data.csv            # Sample data untuk testing
├── requirements.txt           # Python dependencies
├── REPORT_GENERATOR_README.md # Dokumentasi lengkap report generator
├── IEEE-dga.csv              # IEEE standards documentation
└── README.md                 # File ini
```


