import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_env_var(key: str, default: Any = None) -> Any:
    """
    Get environment variable with validation
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

def setup_directories() -> Dict[str, Path]:
    """
    Create required directories if they don't exist
    """
    base_dir = Path(__file__).parent.parent
    
    directories = {
        'data': base_dir / 'data',
        'logs': base_dir / 'data' / 'logs',
        'market_data': base_dir / 'data' / 'market_data',
        'model_cache': base_dir / 'ai_model' / 'cache',
    }
    
    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
    
    return directories

def validate_environment() -> None:
    """
    Validate required environment variables and directories
    """
    required_vars = [
        'OPENSERV_API_KEY',
        'GEMINI_API_KEY',
        'BOT_TOKEN',
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Setup directories
    setup_directories() 