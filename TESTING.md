# 🧪 Testing RizBot

This document provides testing instructions for RizBot Deep Learning Chatbot.

## Quick Test

Run the comprehensive demo:
```bash
python demo.py
```

## Manual Testing

### 1. Test Training Process
```bash
python train.py
# Select option 1 for advanced training
# Select option 3 for quick test
```

### 2. Test Interactive Chat
```bash
python chatbot.py
```

Sample conversations to test:
- `Hello` → Should detect greeting intent
- `vibration analysis` → Should detect vibration_analysis intent
- `MCSA motor` → Should detect mcsa_analysis intent
- `maintenance recommendation` → Should detect maintenance_recommendation intent
- `help` → Should detect help intent
- `bye` → Should detect goodbye intent

### 3. Test Model Persistence
```bash
# Train and save model
python -c "from src.deep_learning_chatbot import train_new_model; train_new_model()"

# Load saved model
python -c "from src.deep_learning_chatbot import PdMChatbot; bot = PdMChatbot(); print('Load success:', bot.load_model())"
```

### 4. Test Data Generation
```bash
python -c "from src.data_generator import main; main()"
```

## Expected Results

### Model Performance
- **Training Accuracy**: >85% after 30 epochs
- **Intent Classification**: >70% confidence for correct intents
- **Response Time**: <100ms per query
- **Model Size**: ~2MB total (H5 + pickle files)

### Intent Detection
- **Greeting**: "hi", "hello", "halo" → high confidence
- **Vibration**: "vibration", "getaran", "bearing" → high confidence  
- **MCSA**: "current", "motor", "electrical" → high confidence
- **DGA**: "gas", "transformer", "oil" → high confidence
- **Maintenance**: "maintenance", "perawatan", "predictive" → high confidence
- **Help**: "help", "bantuan", "what can you do" → high confidence
- **Goodbye**: "bye", "goodbye", "thanks" → high confidence

### Error Handling
- Unknown inputs should return confidence < 0.5
- NLTK data should auto-download if missing
- Model should auto-train if not found

## Troubleshooting

### Common Issues
1. **ImportError**: Run `pip install -r requirements.txt`
2. **NLTK Error**: Run `python -c "import nltk; nltk.download('all')"`
3. **Low Confidence**: Add more training patterns in `data/intents.json`
4. **Model Not Found**: Run training script first

### Performance Tuning
- Increase epochs for better accuracy
- Add more training patterns for specific intents
- Adjust confidence threshold in `classify_intent()`
- Use larger hidden layers for more complex patterns