from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Remove keyboard
remove_keyboard = ReplyKeyboardRemove()

# Language selection
def get_language_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="🇬🇧 English"))
    keyboard.add(KeyboardButton(text="🇪🇹 Amharic"))
    keyboard.add(KeyboardButton(text="🇪🇹 Affan Oromo"))
    keyboard.add(KeyboardButton(text="🇪🇹 Tigrinya"))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)

# Gender selection
def get_gender_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="Male"))
    keyboard.add(KeyboardButton(text="Female"))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)

# Religion selection
def get_religion_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="☪️ Muslim"))
    keyboard.add(KeyboardButton(text="✝️ Christian Orthodox"))
    keyboard.add(KeyboardButton(text="✝️ Christian Protestant"))
    keyboard.add(KeyboardButton(text="✡️ Jewish"))
    keyboard.add(KeyboardButton(text="🕉️ Hindu"))
    keyboard.add(KeyboardButton(text="☸️ Buddhist"))
    keyboard.add(KeyboardButton(text="🚫 Other"))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)

# Location sharing
def get_location_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="📍 Share Location", request_location=True))
    cities = [
        "Addis Ababa", "Dire Dawa", "Mekelle", "Gondar", "Awassa",
        "Bahir Dar", "Jimma", "Dessie", "Jijiga", "Shashamane",
        "Arba Minch", "Hosaena", "Harar", "Nekemte", "Adama"
    ]
    for city in cities:
        keyboard.add(KeyboardButton(text=city))
    keyboard.adjust(1,2)
    # keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)

# Ethiopian cities
def get_cities_keyboard():
    keyboard = ReplyKeyboardBuilder()
    cities = [
        "Addis Ababa", "Dire Dawa", "Mekelle", "Gondar", "Awassa",
        "Bahir Dar", "Jimma", "Dessie", "Jijiga", "Shashamane",
        "Arba Minch", "Hosaena", "Harar", "Nekemte", "Adama"
    ]
    for city in cities:
        keyboard.add(KeyboardButton(text=city))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)

# # Main menu
# def get_main_menu_keyboard():
#     keyboard = ReplyKeyboardBuilder()
#     keyboard.add(KeyboardButton(text="🔍 Find Matches"))
#     keyboard.add(KeyboardButton(text="👤 My Profile"))
#     keyboard.add(KeyboardButton(text="💌 My Messages"))
#     keyboard.adjust(2)
#     return keyboard.as_markup(resize_keyboard=True)