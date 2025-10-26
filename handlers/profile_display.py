import logging
import time
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from database import db
from config import config
from keyboards.inline import (
    get_coin_packages_keyboard,
    get_profile_actions_keyboard, 
    get_message_actions_keyboard, 
    get_cancel_keyboard
)
from utils.helpers import format_profile_html, format_profile_safe, parse_photos, user_state
from utils.translations import get_text, get_user_language

router = Router()

class MessageStates(StatesGroup):
    waiting_for_message = State()

# Global state to track user's current viewing session
user_viewing_sessions = {}

async def start_profile_session(user_id: int, profiles: list, session_type: str = "search"):
    """Start or update a profile viewing session for a user"""
    user_viewing_sessions[user_id] = {
        "profiles": profiles,
        "current_index": 0,
        "session_type": session_type,
        "last_fetch_time": time.time(),
        "is_active": True
    }
    return user_viewing_sessions[user_id]

async def get_current_session(user_id: int):
    """Get current viewing session for user"""
    return user_viewing_sessions.get(user_id)

async def update_session_index(user_id: int, new_index: int):
    """Update the current index in user's session"""
    if user_id in user_viewing_sessions:
        user_viewing_sessions[user_id]["current_index"] = new_index
        return True
    return False

async def clear_session(user_id: int):
    """Clear user's viewing session"""
    if user_id in user_viewing_sessions:
        del user_viewing_sessions[user_id]

async def show_profile_by_index(message: Message, user_id: int, index: int = None):
    """Show profile at specific index in current session"""
    session = await get_current_session(user_id)
    user_lang = get_user_language(user_id, db)
    
    if not session or not session.get("is_active"):
        await message.answer(get_text('no_active_session', user_lang))
        return False
    
    profiles = session["profiles"]
    
    # Use provided index or current index
    if index is None:
        index = session["current_index"]
    
    if index >= len(profiles):
        # End of profiles reached
        await handle_end_of_profiles(message, user_id, session)
        return False
    
    profile = profiles[index]
    await display_single_profile(message, profile, user_lang, index + 1, len(profiles))
    
    # Update the session index
    await update_session_index(user_id, index)
    return True

async def show_next_profile(message: Message, user_id: int):
    """Show next profile in current session"""
    session = await get_current_session(user_id)
    if not session:
        return False
    
    next_index = session["current_index"] + 1
    return await show_profile_by_index(message, user_id, next_index)

async def display_single_profile(message: Message, profile: dict, user_lang: str, current_num: int, total: int):
    """Display a single profile with proper formatting"""
    profile_text = format_profile_html(profile, user_lang)
    profile_text += f"\n\n📊 {current_num}/{total}"
    
    photos = parse_photos(profile.get('photos', '[]'))
    
    try:
        if photos and len(photos) >= 2:
            media_group = []
            media_group.append(
                InputMediaPhoto(
                    media=photos[0],
                    caption=profile_text
                )
            )
            media_group.append(
                InputMediaPhoto(media=photos[1])
            )
            
            await message.bot.send_media_group(
                chat_id=message.chat.id,
                media=media_group
            )
            
            await message.answer(
                get_text('action_prompt', user_lang),
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
            
        elif photos:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=photos[0],
                caption=profile_text,
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
        else:
            await message.answer(
                profile_text,
                reply_markup=get_profile_actions_keyboard(profile['user_id'])
            )
        
    except Exception as e:
        logging.error(f"Error displaying profile: {e}")
        # Fallback
        simple_text = f"👤 {profile.get('first_name', get_text('unknown_user', user_lang))}"
        if profile.get('age'):
            simple_text += f", {profile['age']}"
        simple_text += f"\n\n📊 {current_num}/{total}"
        
        await message.answer(
            simple_text,
            reply_markup=get_profile_actions_keyboard(profile['user_id'])
        )

async def handle_end_of_profiles(message: Message, user_id: int, session: dict):
    """Handle when user reaches end of profile list"""
    user_lang = get_user_language(user_id, db)
    session_type = session.get("session_type", "search")
    
    # Check if we should refetch or show cooldown
    last_fetch_time = session.get("last_fetch_time", 0)
    current_time = time.time()
    time_since_last_fetch = current_time - last_fetch_time
    
    # 30-second cooldown before refetching
    if time_since_last_fetch < 30:
        cooldown_remaining = 30 - int(time_since_last_fetch)
        await message.answer(
            get_text('all_profiles_seen_cooldown', user_lang, seconds=cooldown_remaining),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=get_text('try_again_later', user_lang),
                            callback_data="try_again_later"
                        )
                    ]
                ]
            )
        )
        # Keep session active but mark as ended
        session["is_active"] = False
    else:
        # Try to refetch new profiles
        await refetch_and_continue(message, user_id, session_type, user_lang)

async def refetch_and_continue(message: Message, user_id: int, session_type: str, user_lang: str):
    """Refetch profiles and continue showing"""
    user_data = db.get_user(user_id)
    
    if not user_data or not user_data.get('gender'):
        await message.answer(get_text('profile_setup_required', user_lang))
        await clear_session(user_id)
        return
    
    # Fetch new matches based on session type
    if session_type == "search":
        new_profiles = db.get_users_for_matching(user_id, user_data['gender'])
    elif session_type == "likes":
        new_profiles = db.get_user_likes(user_id)
    else:
        new_profiles = []
    
    if new_profiles:
        # Start new session with fresh profiles
        await start_profile_session(user_id, new_profiles, session_type)
        await show_profile_by_index(message, user_id, 0)
        await message.answer(get_text('new_profiles_found', user_lang, count=len(new_profiles)))
    else:
        await message.answer(get_text('no_fresh_matches', user_lang))
        await clear_session(user_id)

async def browse_profiles_for_user(callback: CallbackQuery, user_id: int):
    """Browse profiles for a specific user from callback context"""
    user_lang = get_user_language(user_id, db)
    user_data = db.get_user(user_id)
    
    print(f"DEBUG: browse_profiles_for_user - User ID: {user_id}")
    print(f"DEBUG: User data: {user_data}")
    
    if not user_data:
        await callback.message.answer(get_text('incomplete_registration', user_lang))
        return
    
    if not user_data.get('photos'):
        await callback.message.answer(get_text('no_photos_profile', user_lang))
        return
    
    if not user_data.get('gender'):
        await callback.message.answer(get_text('incomplete_profile', user_lang))
        return
    
    # Get potential matches
    matches = db.get_users_for_matching(user_id, user_data['gender'])
    
    if not matches:
        await callback.message.answer(get_text('no_matches_found', user_lang))
        return
    
    # Start viewing session
    await start_profile_session(user_id, matches, "search")
    await show_profile_by_index(callback.message, user_id, 0)

# Like/Skip handlers - these work for ANY profile source
@router.callback_query(F.data.startswith("like_"))
async def process_like(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, db)
    liked_user_id = int(callback.data.split("_")[1])
    
    # Add like to database
    success = db.add_like(user_id, liked_user_id)
    
    if success:
        await callback.answer(get_text('like_sent', user_lang))
    else:
        await callback.answer(get_text('already_liked', user_lang))
    
    # Show next profile regardless of source
    await show_next_profile(callback.message, user_id)

@router.callback_query(F.data.startswith("skip_"))
async def process_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, db)
    
    await callback.answer(get_text('skipped', user_lang))
    await show_next_profile(callback.message, user_id)

@router.callback_query(F.data == "try_again_later")
async def try_again_later(callback: CallbackQuery):
    """Handle try again button"""
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, db)
    
    session = await get_current_session(user_id)
    if session:
        await refetch_and_continue(callback.message, user_id, session["session_type"], user_lang)
    else:
        await callback.answer(get_text('session_expired', user_lang))

# Message handling (keep your existing message handlers)
@router.callback_query(F.data.startswith("message_"))
async def process_message_init(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id, db)
    to_user_id = int(callback.data.split("_")[1])
    to_user_data = db.get_user(to_user_id)
    
    if not to_user_data:
        await callback.answer(get_text('user_not_found', user_lang))
        return
    
    await state.set_state(MessageStates.waiting_for_message)
    await state.update_data(to_user_id=to_user_id)
    
    await callback.message.answer(
        get_text('write_message_to', user_lang, first_name=to_user_data['first_name']),
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()

@router.message(MessageStates.waiting_for_message)
async def process_message_send(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    user_data = await state.get_data()
    to_user_id = user_data.get('to_user_id')
    
    if not to_user_id:
        await message.answer(get_text('error_try_again', user_lang))
        await state.clear()
        return
    
    # Check coins and send message (your existing logic)
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
    
    success = db.add_message(message.from_user.id, to_user_id, message.text)
    
    if success:
        db.deduct_user_coins(message.from_user.id, cost)
        from_user_data = db.get_user(message.from_user.id)
        recipient_lang = get_user_language(to_user_id, db)
        
        try:
            await message.bot.send_message(
                chat_id=to_user_id,
                text=f"💌 {get_text('new_message_from', recipient_lang, first_name=from_user_data['first_name'], age=from_user_data.get('age', 'N/A'))}:\n\n"
                     f"\"{message.text}\"",
                reply_markup=get_message_actions_keyboard(message.from_user.id)
            )
            await message.answer(get_text('message_sent', user_lang))
        except:
            await message.answer(get_text('message_delivery_failed', user_lang))
    else:
        await message.answer(get_text('message_send_error', user_lang))
    
    await state.clear()