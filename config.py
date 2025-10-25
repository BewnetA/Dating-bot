import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    ADMIN_ID: int = int(os.getenv('ADMIN_ID', 0))
    
    # Database configuration
    DB_NAME: str = "dating_bot.db"
    
    # Bot settings
    MAX_PHOTOS: int = 5
    MIN_AGE: int = 18
    MAX_AGE: int = 100

config = Config()