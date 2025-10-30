import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    ADMIN_ID: int = int(os.getenv('ADMIN_ID', 0))
    
    # Database configuration
    # DB_NAME: str = "dating_bot.db"
    # PostgreSQL Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'dating_bot')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '*@#$')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # Bot settings
    MAX_PHOTOS: int = 5
    MIN_AGE: int = 18
    MAX_AGE: int = 100
    # In config.py for development
    WEBHOOK_URL = "https://unmollified-ungradually-verna.ngrok-free.dev"  # Get from: ngrok http 8080
    WEBHOOK_PATH = "/webhook"
    WEBAPP_HOST = "0.0.0.0"
    WEBAPP_PORT = 8080
    # Add to your config.py or at the top of handlers file
    COIN_CONFIG = {
        'message_cost': 2,           # Coins per message
        'free_messages': 5,          # Free messages for new users
        'view_all_likers_cost': 10,  # Coins to see all likers
        'free_likers_display': 0,    # Free likers to display
    }

config = Config()