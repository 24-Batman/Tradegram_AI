import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    
    required_vars = [
        'BOT_TOKEN',
        'OPENSERV_API_KEY',
        'GEMINI_API_KEY',
        'API_BASE_URL'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 