# TradeGramAI 🤖

TradeMateAI is an intelligent cryptocurrency trading assistant that provides **market analysis, trading signals, and sentiment analysis** through a Telegram bot interface.

---

## 📊 Features  

- **Market Analysis**: Real-time price data and technical indicators.  
- **Trading Signals**: AI-powered trading recommendations using reinforcement learning.  
- **Sentiment Analysis**: Market sentiment analysis from multiple sources.  
- **Technical Analysis**: Advanced pattern recognition and trend analysis.  

---

## 🛠 Technology Stack  

- **Python 3.8+**  
- **Telegram Bot API**  
- **PyTorch** (AI/ML)  
- **Kraken API** (Market Data)  
- **Reinforcement Learning**  
- **Sentiment Analysis**  

---

## 🚀 Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/yourusername/TradeMateAI.git
cd TradeMateAI
```

### 2️⃣ Create and activate a virtual environment  
#### For Linux/Mac:  
```bash
python -m venv venv
source venv/bin/activate
```
#### For Windows:  
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables  
Create a `.env` file and add the following:  
```env
TELEGRAM_BOT_TOKEN=your_bot_token
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_API_SECRET=your_kraken_api_secret
```

---

## 💡 Usage  

### Start the bot  
```bash
python -m bot.main
```

### Available Commands in Telegram  
- `/start` - Welcome message and introduction  
- `/help` - List all available commands  
- `/market <symbol>` - Get market analysis (e.g., `/market BTC/USD`)  
- `/sentiment <symbol>` - Get sentiment analysis  
- `/trade <symbol>` - Get trading signals  
- `/settings` - View current settings  

---

## 📁 Project Structure  

```
TradeMateAI/
├── agent/
│   ├── agent.py               # Main trading agent logic
│   ├── models.py              # Data models and types
│   └── tasks.py               # Background tasks
├── ai_model/
│   ├── reinforcement.py       # Reinforcement learning model
│   ├── sentiment_analysis.py  # Sentiment analysis logic
│   └── trade_analysis.py      # Trade analysis logic
├── bot/
│   ├── commands.py            # Telegram bot commands
│   ├── main.py                # Bot entry point
│   └── utils.py               # Utility functions
├── data/
│   └── logs/                  # Application logs
└── config/
    └── settings.py            # Configuration settings
```

---

## 🔍 Features in Detail  

### ✅ **Market Analysis**  
- Real-time price data from Kraken  
- Technical indicators (**RSI, MACD, Volume**)  
- Price trend analysis  
- 24-hour price changes  

### ✅ **Trading Signals**  
- AI-powered trading recommendations  
- **Reinforcement learning** for adaptive strategies  
- **Technical analysis** integration  
- Confidence scoring  

### ✅ **Sentiment Analysis**  
- Multi-source **sentiment aggregation**  
- **Confidence scoring** for sentiment analysis  
- **Source tracking** for data reliability  
- Real-time updates  

---

## 🤝 Contributing  

1. **Fork** the repository.  
2. Create your feature branch:  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a **Pull Request**.  

---

## 📝 License  

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

## 🙏 Acknowledgments  

- **Kraken API** for market data.  
- **Telegram Bot API** for the interface.  
- **PyTorch** for AI/ML capabilities.  

---

## ⚠️ Disclaimer  

This bot is for **educational and research purposes only**. Always do your own research and **never trade more than you can afford to lose**. Cryptocurrency trading carries significant risks.  

---

🚀 **Enjoy using TradeGramAI!**  
```

This README provides:  
✅ **Clear project overview**  
✅ **Installation instructions**  
✅ **Usage guide**  
✅ **Project structure**  
✅ **Detailed feature descriptions**  
✅ **Contributing guidelines**  
✅ **Important disclaimers**  

Let me know if you need modifications! 🚀
