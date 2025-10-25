from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from telegram import InputMediaPhoto

from database import db
from utils.helpers import format_profile_safe, parse_photos
from utils.translations import get_text, get_user_language  # ✅ ADD THIS IMPORT

router = Router()

@router.message(F.text == "👤 My Profile")
@router.message(Command("myprofile"))
async def show_profile(message: Message):
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_data = db.get_user(message.from_user.id)
    
    if not user_data:
        await message.answer(get_text('incomplete_profile_registration', user_lang))
        return
    
    profile_text = format_profile_safe(user_data, user_lang)  
    photos = parse_photos(user_data.get('photos', '[]'))
    
    if photos and len(photos) >= 2:
        # Send first 2 photos as media group for user's own profile
        media_group = []
        
        # First photo with profile caption
        media_group.append(
            InputMediaPhoto(
                media=photos[0],
                caption=profile_text
            )  # ✅ FIXED: Remove .to_dict()
        )
        
        # Second photo without caption
        media_group.append(
            InputMediaPhoto(media=photos[1])  # ✅ FIXED: Remove .to_dict()
        )
        
        await message.bot.send_media_group(
            chat_id=message.chat.id,
            media=media_group
        )
        
        # If there are more than 2 photos, mention it
        if len(photos) > 2:
            await message.answer(get_text('total_photos_count', user_lang, count=len(photos)))
        
    elif photos:
        # Only one photo
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=photos[0],
            caption=profile_text
        )
    else:
        # No photos
        await message.answer(profile_text)

@router.message(F.text == "💌 My Messages")
async def show_messages(message: Message):
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(get_text('messages_empty', user_lang))