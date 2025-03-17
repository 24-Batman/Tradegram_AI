# TradeMateAI

A sophisticated AI-powered trading assistant that helps analyze market trends and provide trading recommendations.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API keys
6. Run the bot: `python bot/main.py`

## Features

- Real-time market analysis
- Sentiment analysis of market news
- Trading pattern recognition
- AI-powered trading recommendations
- Telegram bot interface

## Configuration

Update the `.env` file with your API keys and configuration:

- BOT_TOKEN: Your Telegram bot token
- OPENSERV_API_KEY: Your OpenServ API key
- GEMINI_API_KEY: Your Gemini API key
- API_BASE_URL: Base URL for API requests
- PORT: Port for the API server

## License

MIT