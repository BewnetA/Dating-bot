from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

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
    
    # Add user to database
    db.add_user(user_id, username, first_name, last_name)
    
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

@router.message(RegistrationStates.sharing_location, F.text == "🏙️ Choose City")
async def process_city_choice(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id, db)
    
    await message.answer(
        get_text('city_choice_prompt', user_lang),
        reply_markup=get_cities_keyboard()
    )

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
    user_lang = get_user_language(message.from_user.id, db)
    user_data = user_state.get_data(message.from_user.id)
    photos = user_data.get('photos', [])
    
    # Get the highest quality photo
    photo_file_id = message.photo[-1].file_id
    
    # Prevent duplicate photos
    if photo_file_id in photos:
        await message.answer(get_text('duplicate_photo', user_lang))
        return
        
    photos.append(photo_file_id)
    user_state.update_data(message.from_user.id, {"photos": photos})
    
    # Check if we have enough photos AND registration is not already completed
    if len(photos) >= 2 and not user_data.get('registration_completed', False):
        # Mark registration as completed to prevent duplicate messages
        user_state.update_data(message.from_user.id, {"registration_completed": True})
        
        # Save photos to database
        from utils.helpers import save_photos
        photos_str = save_photos(photos)
        success = db.update_user_profile(message.from_user.id, photos=photos_str)
        
        if success:
            # Send completion message ONLY ONCE
            await message.answer(
                f"{get_text('registration_complete', user_lang)}\n\n"
                f"{get_text('registration_success', user_lang)}",
                reply_markup=remove_keyboard
            )
            
            # Clear state and redirect to matches
            await state.clear()
            user_state.clear_state(message.from_user.id)
            
            # Redirect to browse profiles
            await browse_profiles(message)
        else:
            await message.answer(get_text('photos_save_error', user_lang))
    else:
        # Registration already completed, just acknowledge the additional photo
        await message.answer(get_text('photo_added', user_lang))