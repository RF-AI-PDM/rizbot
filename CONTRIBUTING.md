# Contributing to RizBot

Terima kasih atas ketertarikan Anda untuk berkontribusi pada RizBot! 🎉

## 🤝 Cara Berkontribusi

### 1. Fork Repository
Fork repository ini ke akun GitHub Anda.

### 2. Clone Fork Anda
```bash
git clone https://github.com/YOUR_USERNAME/rizbot.git
cd rizbot
```

### 3. Buat Branch Baru
```bash
git checkout -b feature/nama-fitur-anda
```

### 4. Setup Development Environment
```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 5. Make Your Changes

#### Menambah Intent Baru
Edit file `intents.json` dan tambahkan intent baru:
```json
{
  "tag": "new_intent",
  "patterns": [
    "pattern 1",
    "pattern 2"
  ],
  "responses": [
    "response 1",
    "response 2"
  ]
}
```

#### Memodifikasi Chatbot Logic
Edit file `chatbot.py` untuk menambah fitur atau memperbaiki bug.

### 6. Test Your Changes
```bash
# Test chatbot
python chatbot.py

# Test programmatically
python example.py
```

### 7. Commit Changes
```bash
git add .
git commit -m "Add: deskripsi singkat perubahan"
```

Gunakan conventional commits:
- `Add:` untuk fitur baru
- `Fix:` untuk bug fixes
- `Update:` untuk perubahan existing features
- `Docs:` untuk dokumentasi
- `Refactor:` untuk refactoring code

### 8. Push ke Fork Anda
```bash
git push origin feature/nama-fitur-anda
```

### 9. Buat Pull Request
Buka repository asli dan buat Pull Request dari branch Anda.

## 📋 Guidelines

### Code Style
- Ikuti PEP 8 untuk Python code
- Gunakan docstrings untuk functions dan classes
- Tambahkan comments untuk logic yang kompleks
- Gunakan meaningful variable names

### Intent Guidelines
- Patterns harus dalam Bahasa Indonesia (bilingual support coming soon)
- Minimal 3 patterns per intent
- Minimal 2 responses per intent
- Responses harus informatif dan mudah dipahami

### Testing
- Test chatbot secara manual sebelum commit
- Pastikan tidak ada error atau exception
- Test dengan berbagai variasi input

### Documentation
- Update README.md jika menambah fitur besar
- Tambahkan docstrings untuk functions baru
- Update CHANGELOG jika ada (coming soon)

## 🐛 Reporting Bugs

Jika menemukan bug, buat Issue dengan informasi:
1. Deskripsi bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Python version & OS
6. Error messages (jika ada)

## 💡 Suggesting Features

Buat Issue dengan label `enhancement` dan jelaskan:
1. Fitur yang diinginkan
2. Use case / alasan
3. Contoh implementasi (jika ada)

## 🎯 Priority Areas

Area yang membutuhkan kontribusi:
- [ ] Machine Learning untuk intent classification
- [ ] Integration dengan data CSV/PDF
- [ ] Web interface (Streamlit/Flask)
- [ ] English language support
- [ ] More intents untuk PdM topics
- [ ] Unit tests
- [ ] CI/CD setup

## 📞 Questions?

Jika ada pertanyaan, buat Issue dengan label `question` atau hubungi maintainers.

## 📜 Code of Conduct

Harap ikuti [Code of Conduct](CODE_OF_CONDUCT) kami dalam semua interaksi.

---

**Terima kasih telah berkontribusi! 🙏**
