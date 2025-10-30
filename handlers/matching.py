import logging
import random as rd
import time
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from database import db
from config import config
from handlers.commands import display_liker_profile
from keyboards.inline import (
    get_coin_packages_keyboard,
    get_profile_actions_keyboard, 
    get_message_actions_keyboard, 
    get_cancel_keyboard
)
from utils.helpers import format_profile_html, format_profile_safe, parse_photos, user_state
from utils.translations import get_text, get_user_language  # ✅ ADD THIS IMPORT

router = Router()

class MessageStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_media_message = State()  # For non-text messages

# Reusable function to show browse profiles that can be called from complete registration function
async def show_browse_profiles(message: Message, user_id: int = None):
    """Reusable function to show browse profiles"""
    if user_id is None:
        user_id = message.from_user.id
        
    user_lang = get_user_language(user_id, db)
    user_data = db.get_user(user_id)
    
    if not user_data:
        await message.answer(get_text('incomplete_registration', user_lang))
        return False
    
    if not user_data.get('photos'):
        await message.answer(get_text('no_photos_profile', user_lang))
        return False
    
    if not user_data.get('gender'):
        await message.answer(get_text('incomplete_profile', user_lang))
        return False
    
    # Get potential matches
    matches = db.get_users_for_matching(user_id, user_data['gender'])
        
    if not isinstance(matches, list):
        await message.answer("❌ Error: Could not load matches")
        return False
    
    if not matches:
        await message.answer(get_text('no_matches_found', user_lang))
        return False
    
    # ✅ Now shuffle the actual list
    rd.shuffle(matches)
    
    user_state.update_data(
        user_id,
        {
            "current_matches": matches,
            "current_index": 0
        }
    )
    
    # Show first match
    await show_next_profile(message, matches, 0)
    return True

@router.message(F.text == "🔍 Find Matches")
@router.message(Command("search"))
async def browse_profiles(message: Message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, db)
    user_data = db.get_user(user_id)
    
    if not user_data:
        await message.answer(get_text('incomplete_registration', user_lang))
        return
    
    if not user_data.get('photos'):
        await message.answer(get_text('no_photos_profile', user_lang))
        return
    
    if not user_data.get('gender'):
        await message.answer(get_text('incomplete_profile', user_lang))
        return
    
    # Get potential matches - MAKE SURE IT'S CALLED AS A FUNCTION
    matches = db.get_users_for_matching(user_id, user_data['gender'])
        
    # Check if matches is actually a list
    if not isinstance(matches, list):
        await message.answer("❌ Error: Could not load matches")
        return
    
    if not matches:
        await message.answer(get_text('no_matches_found', user_lang))
        return
    
    # ✅ Now shuffle the actual list
    rd.shuffle(matches)
    
    user_state.update_data(
        user_id,
        {
            "current_matches": matches,
            "current_index": 0
        }
    )
    
    # Show first match
    await show_next_profile(message, matches, 0)
    
async def show_next_profile(message: Message, matches: list, current_index: int = 0):
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    if current_index >= len(matches):
        await message.answer(get_text('all_profiles_seen', user_lang))
        return
    
    profile = matches[current_index]
    profile_text = format_profile_html(profile, user_lang)
    
    # Get photos
    photos = parse_photos(profile.get('photos', '[]'))
    
    try:
        if photos and len(photos) >= 2:
            # Send first 2 photos as media group with profile info on first photo
            media_group = []
            
            # First photo with profile caption
            media_group.append(
                InputMediaPhoto(
                    media=photos[0],
                    caption=profile_text
                )
            )
            
            # Second photo without caption
            media_group.append(
                InputMediaPhoto(media=photos[1])
            )
            
            # Send the media group (2 photos together)
            await message.bot.send_media_group(
                chat_id=message.chat.id,
                media=media_group
            )
            
            # Send action buttons separately with engaging text
            await message.answer(
                get_text('action_prompt', user_lang),
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
            
        elif photos:
            # Only one photo - send with caption and buttons
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=photos[0],
                caption=profile_text,
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
        else:
            # No photos available
            await message.answer(
                profile_text,
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
        
        # Store current match index for navigation
        user_state.update_data(
            message.from_user.id, 
            {
                "current_matches": matches,
                "current_index": current_index
            }
        )
        
    except Exception as e:
        logging.error(f"Error showing profile: {e}")
        # Fallback to simple display
        simple_text = f"👤 {profile.get('first_name', get_text('unknown_user', user_lang))}"
        if profile.get('age'):
            simple_text += f", {profile['age']}"
        
        try:
            if photos:
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photos[0],
                    caption=simple_text,
                    reply_markup=get_profile_actions_keyboard(profile['user_id'])
                )
            else:
                await message.answer(
                    simple_text,
                    reply_markup=get_profile_actions_keyboard(profile['user_id'])
                )
            
            # Store current match index for navigation
            user_state.update_data(
                message.from_user.id, 
                {
                    "current_matches": matches,
                    "current_index": current_index
                }
            )
        except Exception as e2:
            logging.error(f"Even simple text failed: {e2}")
            await message.answer(get_text('profile_display_error', user_lang))

@router.callback_query(F.data.startswith("like_"))
async def process_like(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, db)  # ✅ GET USER LANGUAGE
    liked_user_id = int(callback.data.split("_")[1])
    
    # Add like to database
    success = db.add_like(user_id, liked_user_id)
    
    if success:
        await callback.answer(get_text('like_sent', user_lang))
    else:
        await callback.answer(get_text('already_liked', user_lang))
    
    # Show next profile
    await show_next_after_action(callback, user_id)

@router.callback_query(F.data.startswith("skip_"))
async def process_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, db)  # ✅ GET USER LANGUAGE
    
    await callback.answer(get_text('skipped', user_lang))
    await show_next_after_action(callback, user_id)

async def show_next_after_action(callback: CallbackQuery, user_id: int):
    """Show next profile with random shuffle (no cooldown needed)"""
    user_lang = get_user_language(user_id, db)
    user_data = user_state.get_data(user_id)
    
    matches = user_data.get('current_matches', [])
    current_index = user_data.get('current_index', 0) + 1
        
    # Check if we've reached the end of current matches
    if current_index >= len(matches):
        await callback.answer(get_text('fetching_matches', user_lang))
        
        user_profile_data = db.get_user(user_id)
        if not user_profile_data or not user_profile_data.get('gender'):
            await callback.answer(get_text('profile_setup_required', user_lang), show_alert=True)
            return
        
        fresh_matches = db.get_users_for_matching(user_id, user_profile_data['gender'])
        
        if not fresh_matches:
            await callback.answer(get_text('no_matches', user_lang), show_alert=True)
            # Update state to prevent continuous refetch attempts
            user_state.update_data(user_id, {
                "current_matches": matches,
                "current_index": current_index
            })
            return
        
        # ✅ Shuffle the fresh matches for random order
        rd.shuffle(fresh_matches)
        matches = fresh_matches
        current_index = 0
    
    # Always update state
    user_state.update_data(user_id, {
        "current_matches": matches,
        "current_index": current_index
    })
    
    await show_next_profile(callback.message, matches, current_index)
    
@router.callback_query(F.data.startswith("message_"))
async def process_message_init(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id, db)
    to_user_id = int(callback.data.split("_")[1])
    to_user_data = db.get_user(to_user_id)
    
    if not to_user_data:
        await callback.answer(get_text('user_not_found', user_lang))
        return
    
    await state.set_state(MessageStates.waiting_for_media_message)
    await state.update_data(to_user_id=to_user_id)
    
    await callback.message.answer(
        get_text('write_message_to', user_lang, first_name=to_user_data['first_name']),
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()

@router.message(MessageStates.waiting_for_media_message)
async def process_media_message_send(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    user_data = await state.get_data()
    to_user_id = user_data.get('to_user_id')
    
    if not to_user_id:
        await message.answer(get_text('error_try_again', user_lang))
        await state.clear()
        return
    
    # Check coins
    user_info = db.get_user(message.from_user.id)
    user_coins = user_info.get('coins', 0)
    cost = config.COIN_CONFIG['message_cost']
    
    if user_coins < cost:
        await message.answer(
            f"{get_text('insufficient_coins_for_message', user_lang, cost=cost)} \n\n {get_text('buy_coins', user_lang)}",
            reply_markup=get_coin_packages_keyboard()
        )
        await state.clear()
        return
    
    # Process different message types
    success = await process_and_send_media_message(message, to_user_id, user_lang)
    
    if success:
        # Deduct coins only if message was sent successfully
        db.deduct_user_coins(message.from_user.id, cost)
        await message.answer(get_text('message_sent', user_lang))
    else:
        await message.answer(get_text('message_send_error', user_lang))
    
    await state.clear()

async def process_and_send_media_message(message: Message, to_user_id: int, user_lang: str) -> bool:
    """Process and send any type of message (text, photo, video, voice, sticker, etc.)"""
    try:
        from_user_data = db.get_user(message.from_user.id)
        recipient_lang = get_user_language(to_user_id, db)
        
        # Header text for all message types
        header_text = f"💌 {get_text('new_message_from', recipient_lang, first_name=from_user_data['first_name'], age=from_user_data.get('age', 'N/A'))}:\n\n"
        
        # Handle different message types
        if message.text:
            # Text message
            message_text = f"{header_text}\"{message.text}\""
            await message.bot.send_message(
                chat_id=to_user_id,
                text=message_text,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            return db.add_message(message.from_user.id, to_user_id, f"📝 {message.text}")
            
        elif message.photo:
            # Photo with optional caption
            caption = f"{header_text}{message.caption}" if message.caption else header_text
            await message.bot.send_photo(
                chat_id=to_user_id,
                photo=message.photo[-1].file_id,  # Highest quality photo
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            caption_text = f"📷 {message.caption}" if message.caption else "📷 Photo"
            return db.add_message(message.from_user.id, to_user_id, caption_text)
            
        elif message.video:
            # Video with optional caption
            caption = f"{header_text}{message.caption}" if message.caption else header_text
            await message.bot.send_video(
                chat_id=to_user_id,
                video=message.video.file_id,
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            caption_text = f"🎥 {message.caption}" if message.caption else "🎥 Video"
            return db.add_message(message.from_user.id, to_user_id, caption_text)
            
        elif message.voice:
            # Voice message with optional caption
            caption = header_text if header_text else None
            await message.bot.send_voice(
                chat_id=to_user_id,
                voice=message.voice.file_id,
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            return db.add_message(message.from_user.id, to_user_id, "🎤 Voice message")
            
        elif message.audio:
            # Audio file with optional caption
            caption = f"{header_text}{message.caption}" if message.caption else header_text
            await message.bot.send_audio(
                chat_id=to_user_id,
                audio=message.audio.file_id,
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            caption_text = f"🎵 {message.caption}" if message.caption else "🎵 Audio"
            return db.add_message(message.from_user.id, to_user_id, caption_text)
            
        elif message.document:
            # Document with optional caption
            caption = f"{header_text}{message.caption}" if message.caption else header_text
            await message.bot.send_document(
                chat_id=to_user_id,
                document=message.document.file_id,
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            caption_text = f"📄 {message.caption}" if message.caption else "📄 Document"
            return db.add_message(message.from_user.id, to_user_id, caption_text)
            
        elif message.sticker:
            # Sticker
            await message.bot.send_sticker(
                chat_id=to_user_id,
                sticker=message.sticker.file_id,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            return db.add_message(message.from_user.id, to_user_id, "😊 Sticker")
            
        elif message.animation:  # GIF
            # GIF with optional caption
            caption = f"{header_text}{message.caption}" if message.caption else header_text
            await message.bot.send_animation(
                chat_id=to_user_id,
                animation=message.animation.file_id,
                caption=caption,
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            # Save to database
            caption_text = f"🎬 {message.caption}" if message.caption else "🎬 GIF"
            return db.add_message(message.from_user.id, to_user_id, caption_text)
            
        else:
            # Unsupported message type
            await message.answer(get_text('unsupported_message_type', user_lang))
            return False
            
    except Exception as e:
        logging.error(f"Error sending media message: {e}")
        await message.answer(get_text('message_delivery_failed', user_lang))
        return False

@router.callback_query(F.data.startswith("reply_"))
async def process_reply_init(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id, db)
    to_user_id = int(callback.data.split("_")[1])
    to_user_data = db.get_user(to_user_id)
    
    await state.set_state(MessageStates.waiting_for_media_message)
    await state.update_data(to_user_id=to_user_id)
    
    await callback.message.answer(
        get_text('write_reply_to', user_lang, first_name=to_user_data['first_name']),
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()
        

@router.callback_query(F.data.startswith("view_"))
async def process_view_profile(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGEprint(f"DEBUG: callback.data = {callback.data}")
    
    # Get the last part as user ID
    parts = callback.data.split("_")
    
    # The user ID should be the last part
    profile_user_id = int(parts[-1])
    profile_data = db.get_user(profile_user_id)
    
    if not profile_data:
        await callback.answer(get_text('profile_not_found', user_lang))
        return
    
    profile_text = format_profile_html(profile_data, user_lang)
    photos = parse_photos(profile_data.get('photos', '[]'))
    
    try:
        if photos and len(photos) >= 2:
            # Send first 2 photos as media group for user's own profile
            media_group = []
            
            # First photo with profile caption
            media_group.append(
                InputMediaPhoto(
                    media=photos[0],
                    caption=profile_text
                )
            )
            
            # Second photo without caption
            media_group.append(
                InputMediaPhoto(media=photos[1])
            )
            
            await callback.bot.send_media_group(
                chat_id=callback.from_user.id,
                media=media_group
            )
            
            # If there are more than 2 photos, mention it
            if len(photos) > 2:
                await callback.message.answer(get_text('total_photos', user_lang, count=len(photos)))
            
        elif photos:
            # Only one photo
            await callback.bot.send_photo(
                chat_id=callback.from_user.id,
                photo=photos[0],
                caption=profile_text
            )
        else:
            # No photos
            await callback.message.answer(profile_text)
        
        await callback.answer()
    except Exception as e:
        await callback.answer(get_text('profile_error', user_lang))
        logging.error(f"Error in view_profile: {e}")

@router.callback_query(F.data.startswith("block_"))
async def process_block(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    blocked_user_id = int(callback.data.split("_")[1])
    
    success = db.add_block(callback.from_user.id, blocked_user_id)
    
    if success:
        await callback.answer(get_text('user_blocked', user_lang))
        await callback.message.answer(get_text('block_success', user_lang))
    else:
        await callback.answer(get_text('block_error', user_lang))

@router.callback_query(F.data == "cancel")
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await state.clear()
    await callback.message.answer(get_text('cancelled', user_lang))
    await callback.answer()