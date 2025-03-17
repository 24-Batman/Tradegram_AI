import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data directories
MARKET_DATA_DIR = ROOT_DIR / "data" / "market_data"
LOGS_DIR = ROOT_DIR / "data" / "logs"

# Ensure directories exist
MARKET_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True) 