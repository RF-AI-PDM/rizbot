# 🤖 RizBot - Deep Learning Chatbot untuk Predictive Maintenance

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.12%2B-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**RizBot** adalah chatbot berbasis Deep Learning yang dirancang khusus untuk **Predictive Maintenance (PdM)**. Bot ini menggunakan Neural Network untuk memahami pertanyaan teknis dan memberikan analisis serta rekomendasi maintenance yang akurat.

## ✨ Fitur Utama

- 🧠 **Deep Learning Architecture** - Neural Network dengan TensorFlow/Keras
- 🔧 **Vibration Analysis** - Analisis getaran dan diagnosis bearing
- ⚡ **Motor Current Signature Analysis (MCSA)** - Deteksi fault motor listrik
- 🛢️ **Dissolved Gas Analysis (DGA)** - Analisis kondisi transformer
- 📊 **Maintenance Recommendations** - Saran perawatan berdasarkan kondisi
- 🎯 **Intent Classification** - Klasifikasi maksud dengan confidence scoring
- 🚀 **Continuous Learning** - Model dapat dilatih ulang dengan data baru

## 🏗️ Arsitektur System

```
RizBot Architecture:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Deep Learning   │───▶│   Response      │
│   (Text/Voice)  │    │   Intent Model   │    │   Generation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Knowledge Base  │
                       │   (Intents.json) │
                       └──────────────────┘
```

## 📂 Struktur Project

```
rizbot/
├── 📁 data/
│   ├── intents.json              # Training data (intents & responses)
│   └── enhanced_intents.json     # Extended training data
├── 📁 src/
│   ├── deep_learning_chatbot.py  # Core DL chatbot engine
│   └── data_generator.py         # Training data generator
├── 📁 models/
│   ├── chatbot_model.h5          # Trained neural network
│   ├── words.pkl                 # Vocabulary data
│   ├── classes.pkl               # Intent classes
│   └── training_history.png      # Training visualization
├── chatbot.py                    # Main CLI interface
├── train.py                      # Model training script
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/RF-AI-PDM/rizbot.git
cd rizbot

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (otomatis saat first run)
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

### 2. Running RizBot

```bash
# Jalankan chatbot (training otomatis jika model belum ada)
python chatbot.py

# Atau training manual terlebih dahulu
python train.py
```

### 3. First Interaction

```
🤖 RizBot: Halo! Saya RizBot, asisten PdM Anda. Bagaimana saya bisa membantu?

👤 Anda: Bagaimana cara analisis vibrasi bearing?

🤖 RizBot: Analisis vibrasi sangat penting untuk PdM. Saya dapat membantu 
menganalisis spektrum frekuensi, RMS values, dan peak amplitudes...
```

## 🧠 Deep Learning Model

### Architecture Details

```python
Model: Sequential
┌─────────────────────────────────────┐
│ Dense(128, activation='relu')       │  # Input layer
│ Dropout(0.5)                        │  # Regularization
│ Dense(64, activation='relu')        │  # Hidden layer  
│ Dropout(0.5)                        │  # Regularization
│ Dense(n_classes, activation='softmax')│ # Output layer
└─────────────────────────────────────┘

Optimizer: SGD (lr=0.01, momentum=0.9, nesterov=True)
Loss: categorical_crossentropy
Metrics: accuracy
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/new-analysis`)
3. Add training data di `data/intents.json`
4. Test dengan `python train.py`
5. Commit changes (`git commit -m 'Add new analysis feature'`)
6. Push branch (`git push origin feature/new-analysis`)
7. Create Pull Request

## 📄 License

Distributed under MIT License. See `LICENSE` for more information.

---

**🤖 RizBot v1.0** - Powered by Deep Learning & Predictive Maintenance Expertise


