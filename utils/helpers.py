import json
import logging
import html
from typing import List, Optional, Dict, Any
from aiogram.types import Message
from utils.translations import get_text  # ✅ ADD THIS IMPORT

def escape_markdown_v2(text: str) -> str:
    """Escape special MarkdownV2 characters"""
    if not text:
        return ""
    
    # List of special MarkdownV2 characters that need to be escaped
    escape_chars = r'[_*[\]()~`>#+\-=|{}.!]'
    import re
    return re.sub(escape_chars, r'\\\g<0>', text)

def format_profile_safe(user_data: dict, language: str = 'english') -> str:
    """Format user profile in the specified style with real data"""
    from database import db  # Import here to avoid circular imports
    
    first_name = user_data.get('first_name', get_text('profile_unknown', language))
    age = user_data.get('age', '')
    
    # Basic info
    profile_text = f"{first_name}"
    if age:
        profile_text += f" ({age})"
    profile_text += "\n\n"
    
    # Language and location
    user_language = user_data.get('language', 'english').capitalize()
    city = user_data.get('city', get_text('profile_city_not_specified', language))
    
    # ✅ FIX: Changed variable name to avoid conflict
    profile_text += get_text('profile_language', language, profile_language=user_language, city=city) + "\n\n"
    
    # Religion
    religion = user_data.get('religion', get_text('profile_religion_not_specified', language))
    profile_text += f"{religion}\n\n"
    
    # Bio
    bio = user_data.get('bio', '')
    if bio:
        profile_text += f"{bio}\n\n"
    
    # Phone (masked)
    phone = user_data.get('phone', '')
    if phone:
        # Mask phone number, keep last 2 digits
        masked_phone = phone[:4] + '•' * (len(phone) - 5) + phone[-4:-2]
        profile_text += f"📞 {masked_phone}\n\n"
    
    # REAL STATS - Get actual data from database
    user_id = user_data['user_id']
    likes_count = db.get_user_likes_count(user_id)
    matches_count = db.get_user_matches_count(user_id)
    coins_balance = db.get_user_coins(user_id)
    
    # ✅ KEEP EMOJIS AS REQUESTED - Use the specific format with emojis
    profile_text += get_text('profile_stats', language, likes=likes_count, matches=matches_count) + "\n\n"
    profile_text += get_text('profile_balance', language, coins=coins_balance)
    
    return profile_text

def format_profile_html(user_data: dict, language: str = 'english') -> str:  # ✅ ADD LANGUAGE PARAMETER
    """Format user profile using HTML formatting (safer alternative)"""
    first_name = html.escape(user_data.get('first_name', get_text('profile_unknown', language)))
    age = html.escape(str(user_data.get('age', ''))) if user_data.get('age') else ''
    city = html.escape(user_data.get('city', get_text('profile_city_not_specified', language))) if user_data.get('city') else ''
    religion = html.escape(user_data.get('religion', get_text('profile_religion_not_specified', language))) if user_data.get('religion') else ''
    bio = html.escape(user_data.get('bio', '')) if user_data.get('bio') else ''
    
    profile_text = f"👤 <b>{first_name}</b>"
    
    if age:
        profile_text += f", {age}"
    
    if city:
        profile_text += f"\n📍 {city}"
    
    if religion:
        profile_text += f"\n🙏 {religion}"
    
    if bio:
        profile_text += f"\n\n📝 {bio}"
    
    return profile_text

class UserState:
    def __init__(self):
        self.states = {}
    
    def set_state(self, user_id: int, state: str, data: dict = None):
        if user_id not in self.states:
            self.states[user_id] = {}
        self.states[user_id]['state'] = state
        if data:
            self.states[user_id]['data'] = data
    
    def get_state(self, user_id: int) -> Optional[str]:
        user_data = self.states.get(user_id, {})
        return user_data.get('state')
    
    def get_data(self, user_id: int) -> dict:
        user_data = self.states.get(user_id, {})
        return user_data.get('data', {})
    
    def update_data(self, user_id: int, kwargs):
        if user_id not in self.states:
            self.states[user_id] = {'data': {}}
        if 'data' not in self.states[user_id]:
            self.states[user_id]['data'] = {}
        self.states[user_id]['data'].update(kwargs)
    
    def clear_state(self, user_id: int):
        if user_id in self.states:
            del self.states[user_id]

def parse_photos(photos_json: str) -> List[str]:
    """Parse photos from JSON string"""
    try:
        if photos_json:
            return json.loads(photos_json)
        return []
    except (json.JSONDecodeError, TypeError):
        return []

def save_photos(photos_list: List[str]) -> str:
    """Save photos list as JSON string"""
    try:
        return json.dumps(photos_list)
    except Exception as e:
        logging.error(f"Error saving photos: {e}")
        return "[]"

def format_likes_list(likes: List[Dict], language: str = 'english') -> str:  # ✅ ADD LANGUAGE PARAMETER
    """Format list of users who liked the profile"""
    if not likes:
        return get_text('no_likes_yet_list', language)
    
    text = get_text('likes_list_header', language)
    for i, user in enumerate(likes, 1):
        text += f"{i}. {user.get('first_name', get_text('profile_unknown', language))}"
        if user.get('age'):
            text += f", {user['age']}"
        if user.get('city'):
            text += f" - {user['city']}"
        text += "\n"
    
    return text

def format_matches_list(matches: List[Dict], language: str = 'english') -> str:  # ✅ ADD LANGUAGE PARAMETER
    """Format list of mutual matches"""
    if not matches:
        return get_text('no_matches_yet_list', language)
    
    text = get_text('matches_list_header', language)
    for i, match in enumerate(matches, 1):
        text += f"{i}. {match.get('first_name', get_text('profile_unknown', language))}"
        if match.get('age'):
            text += f", {match['age']}"
        if match.get('city'):
            text += f" - {match['city']}"
        text += "\n"
    
    return text

# Global user state manager
user_state = UserState()