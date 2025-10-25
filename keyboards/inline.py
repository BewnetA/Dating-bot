from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Profile actions
def get_profile_actions_keyboard(profile_user_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❤️ Like", callback_data=f"like_{profile_user_id}"))
    keyboard.add(InlineKeyboardButton(text="💌 Message", callback_data=f"message_{profile_user_id}"))
    keyboard.add(InlineKeyboardButton(text="⏭️ Skip", callback_data=f"skip_{profile_user_id}"))
    keyboard.adjust(3)
    return keyboard.as_markup()

# Message actions
def get_message_actions_keyboard(from_user_id: int, message_id: int = None):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="💬 Reply", callback_data=f"reply_{from_user_id}"))
    keyboard.add(InlineKeyboardButton(text="👤 View Profile", callback_data=f"view_{from_user_id}"))
    keyboard.add(InlineKeyboardButton(text="🚫 Block", callback_data=f"block_{from_user_id}"))
    keyboard.adjust(1)
    return keyboard.as_markup()

# Cancel action
def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❌ Cancel", callback_data="cancel"))
    return keyboard.as_markup()

def get_confirm_delete_keyboard():
    """Confirmation keyboard for account deletion"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Yes, Delete My Account", callback_data="confirm_delete_yes"))
    keyboard.add(InlineKeyboardButton(text="❌ No, Keep My Account", callback_data="confirm_delete_no"))
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_coin_packages_keyboard():
    """Keyboard for coin packages"""
    keyboard = InlineKeyboardBuilder()
    packages = [
        ("💰 100 Coins - $4.99", "coins_100"),
        ("💰 250 Coins - $9.99", "coins_250"), 
        ("💰 500 Coins - $17.99", "coins_500"),
        ("💰 1000 Coins - $29.99", "coins_1000"),
        ("💰 2500 Coins - $69.99", "coins_2500")
    ]
    
    for text, code in packages:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=code))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_cancel_keyboard_simple():
    """Simple cancel keyboard"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_operation"))
    return keyboard.as_markup()

def get_payment_approval_keyboard(payment_id: int):
    """Keyboard for admin to approve/reject payments"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Approve", callback_data=f"approve_payment_{payment_id}"))
    keyboard.add(InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_payment_{payment_id}"))
    keyboard.adjust(2)
    return keyboard.as_markup()

def get_cancel_payment_keyboard():
    """Keyboard to cancel payment process"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❌ Cancel Payment", callback_data="cancel_payment"))
    return keyboard.as_markup()