import asyncio
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# Save photos to database
from utils.helpers import save_photos
from database import db
from config import config
from handlers.matching import browse_profiles
from keyboards.reply import *
from keyboards.inline import *
from utils.helpers import user_state
from utils.translations import get_text, get_user_language  # ✅ ADD THIS IMPORT

router = Router()

class RegistrationStates(StatesGroup):
    choosing_language = State()
    entering_name = State()
    sharing_contact = State()
    entering_age = State()
    choosing_gender = State()
    choosing_religion = State()
    sharing_location = State()
    entering_bio = State()
    sharing_photos = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or get_text('no_username', 'english')
    first_name = message.from_user.first_name or "Unknown"
    last_name = message.from_user.last_name or ""
    
    # Check if user already exists and has completed registration
    existing_user = db.get_user(user_id)
    
    if existing_user and existing_user.get('is_active') and existing_user.get('photos'):
        # User is already registered and has photos - redirect to search/browse
        user_lang = get_user_language(user_id, db)
        
        await message.answer(
            get_text('welcome_back', user_lang, first_name=first_name),
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Clear any existing state
        await state.clear()
        
        # Redirect to browse profiles (same as /search command)
        await browse_profiles(message)
        return
    
    # Add/update user in database (for new users or incomplete registration)
    db.add_user(user_id, username, first_name, last_name)
    
    # If user exists but hasn't completed registration, check what's missing
    if existing_user:
        user_lang = get_user_language(user_id, db)
        
        # Check what registration steps are missing
        missing_fields = []
        if not existing_user.get('language'):
            missing_fields.append('language')
        if not existing_user.get('gender'):
            missing_fields.append('gender')
        if not existing_user.get('age'):
            missing_fields.append('age')
        if not existing_user.get('city'):
            missing_fields.append('city')
        if not existing_user.get('bio'):
            missing_fields.append('bio')
        if not existing_user.get('photos'):
            missing_fields.append('photos')
        
        if missing_fields:
            # User exists but registration is incomplete
            await message.answer(
                get_text('registration_incomplete', user_lang),
                reply_markup=get_language_keyboard()
            )
            await state.set_state(RegistrationStates.choosing_language)
            return
    
    # New user - start registration process
    # Notify admin (keep in English)
    if config.ADMIN_ID:
        admin_text = get_text('admin_new_user', 'english', 
                            first_name=first_name, 
                            last_name=last_name,
                            user_id=user_id,
                            username=username)
        try:
            await message.bot.send_message(config.ADMIN_ID, admin_text)
        except Exception as e:
            print(f"Failed to notify admin: {e}")
    
    # Get user language for registration (default to English for new users)
    user_lang = get_user_language(user_id, db)
    
    # Start registration process
    await message.answer(
        f"{get_text('welcome', user_lang)}\n"
        f"{get_text('registration_start', user_lang)}",
        reply_markup=get_language_keyboard()
    )
    await state.set_state(RegistrationStates.choosing_language)

@router.message(RegistrationStates.choosing_language, F.text.in_(["🇬🇧 English", "🇪🇹 Amharic", "🇪🇹 Affan Oromo", "🇪🇹 Tigrinya"]))
async def process_language(message: Message, state: FSMContext):
    language_map = {
        "🇬🇧 English": "english",
        "🇪🇹 Amharic": "amharic", 
        "🇪🇹 Affan Oromo": "oromo",
        "🇪🇹 Tigrinya": "tigrinya"
    }
    
    language = language_map[message.text]
    db.update_user_language(message.from_user.id, language=language)
    user_state.update_data(message.from_user.id, {"language": language})
    
    # Get the updated language for the user
    user_lang = language
    
    await message.answer(
        get_text('name_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(RegistrationStates.entering_name)

@router.message(RegistrationStates.entering_name)
async def process_name(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    name = message.text.strip()
    
    if len(name) < 2:
        await message.answer(get_text('invalid_name', user_lang))
        return
    
    db.update_user_profile(message.from_user.id, first_name=name)
    user_state.update_data(message.from_user.id, {"name": name})
    
    await message.answer(
        get_text('contact_prompt', user_lang),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(
                text=get_text('share_contact_button', user_lang), 
                request_contact=True
            )]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    await state.set_state(RegistrationStates.sharing_contact)

@router.message(RegistrationStates.sharing_contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    contact = message.contact
    phone_number = contact.phone_number
    
    db.update_user_profile(message.from_user.id, phone=phone_number)
    
    await message.answer(
        get_text('age_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(RegistrationStates.entering_age)

@router.message(RegistrationStates.entering_age)
async def process_age(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    
    try:
        age = int(message.text)
        if age < config.MIN_AGE or age > config.MAX_AGE:
            await message.answer(get_text('invalid_age_range', user_lang, 
                                        min_age=config.MIN_AGE, 
                                        max_age=config.MAX_AGE))
            return
    except ValueError:
        await message.answer(get_text('invalid_age_number', user_lang))
        return
    
    db.update_user_profile(message.from_user.id, age=age)
    user_state.update_data(message.from_user.id, {"age": age})
    
    await message.answer(
        get_text('gender_prompt', user_lang),
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(RegistrationStates.choosing_gender)

@router.message(RegistrationStates.choosing_gender, F.text.in_(["Male", "Female"]))
async def process_gender(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    gender = "male" if message.text == "Male" else "female"
    
    db.update_user_profile(message.from_user.id, gender=gender)
    user_state.update_data(message.from_user.id, {"gender": gender})
    
    await message.answer(
        get_text('religion_prompt', user_lang),
        reply_markup=get_religion_keyboard()
    )
    await state.set_state(RegistrationStates.choosing_religion)

@router.message(RegistrationStates.choosing_religion)
async def process_religion(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    religion = message.text
    
    db.update_user_profile(message.from_user.id, religion=religion)
    user_state.update_data(message.from_user.id, {"religion": religion})
    
    await message.answer(
        get_text('location_prompt', user_lang),
        reply_markup=get_location_keyboard()
    )
    await state.set_state(RegistrationStates.sharing_location)

@router.message(RegistrationStates.sharing_location, F.location)
async def process_location(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    
    db.update_user_profile(
        message.from_user.id, 
        latitude=latitude, 
        longitude=longitude,
        city="Shared Location"
    )
    
    await message.answer(
        get_text('bio_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(RegistrationStates.entering_bio)

@router.message(RegistrationStates.sharing_location, F.text)
async def process_city(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    city = message.text
    
    db.update_user_profile(message.from_user.id, city=city)
    user_state.update_data(message.from_user.id, {"city": city})
    
    await message.answer(
        get_text('bio_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(RegistrationStates.entering_bio)

@router.message(RegistrationStates.entering_bio)
async def process_bio(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    bio = message.text
    
    db.update_user_profile(message.from_user.id, bio=bio)
    user_state.update_data(message.from_user.id, {"bio": bio})
    
    await message.answer(
        get_text('photos_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(RegistrationStates.sharing_photos)
    user_state.update_data(message.from_user.id, {"photos": []})

@router.message(RegistrationStates.sharing_photos, F.photo)
async def process_photos(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, db)
    user_data = await state.get_data()
    photos = user_data.get('photos', [])
    
    # Get the highest quality photo
    photo_file_id = message.photo[-1].file_id
    
    # Prevent duplicate photos
    if photo_file_id in photos:
        await message.answer(get_text('duplicate_photo', user_lang))
        return
    
    # STRICTLY limit to maximum 2 photos
    if len(photos) >= 2:
        await message.answer(get_text('max_photos_reached', user_lang))
        return
        
    photos.append(photo_file_id)
    await state.update_data(photos=photos)
    
    # Cancel existing timer if any
    current_timer = user_data.get('photo_timer')
    if current_timer and not current_timer.done():
        current_timer.cancel()
    
    # If first photo, start timer for second photo
    if len(photos) == 1:
        # Create timer task specifically for this user
        timer = asyncio.create_task(photo_timer_handler(user_id, message, state, user_lang))
        await state.update_data(photo_timer=timer, registration_completed=False)
    
    # If second photo received, complete registration immediately
    elif len(photos) == 2:
        await complete_registration(message, state, photos, user_lang)

async def photo_timer_handler(user_id: int, message: Message, state: FSMContext, user_lang: str):
    """Handle the timer for waiting for second photo"""
    try:
        # Wait for specified time
        await asyncio.sleep(3)
        
        # Re-check the current state data to ensure it's still valid
        current_data = await state.get_data()
        current_photos = current_data.get('photos', [])
        
        # Only complete registration if we still have exactly 1 photo and not completed
        if (len(current_photos) == 1 and 
            not current_data.get('registration_completed', False) and
            not current_data.get('photo_timer_cancelled', False)):
            
            await complete_registration(message, state, current_photos, user_lang)
            
    except asyncio.CancelledError:
        # Timer was cancelled because second photo was received
        await state.update_data(photo_timer_cancelled=True)
        pass
    except Exception as e:
        logging.error(f"Timer error for user {user_id}: {e}")

async def complete_registration(message: Message, state: FSMContext, photos: list, user_lang: str):
    """Complete the registration process"""
    user_id = message.from_user.id
    
    # Mark registration as completed to prevent duplicate completion
    await state.update_data(registration_completed=True)
    
    # Clean up timer if exists
    user_data = await state.get_data()
    timer = user_data.get('photo_timer')
    if timer and not timer.done():
        timer.cancel()
    
    # Save photos to database
    photos_str = save_photos(photos)
    success = db.update_user_profile(user_id, photos=photos_str)
    
    if success:
        # Award free coins
        free_coins = config.COIN_CONFIG['message_cost'] * config.COIN_CONFIG['free_messages']
        db.add_user_coins(user_id, free_coins)
            
        await message.answer(
            f"{get_text('registration_complete', user_lang)}\n"
            f"{get_text('free_conis_awarded', user_lang, coins=free_coins)}",
            reply_markup=remove_keyboard
        )
        
        # Clear state
        await state.clear()
        
        # Redirect to browse profiles
        await browse_profiles(message)
    else:
        await message.answer(get_text('photos_save_error', user_lang))