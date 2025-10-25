from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from telegram import InputMediaPhoto

from database import db
from config import config
from keyboards.reply import get_language_keyboard, remove_keyboard
from keyboards.inline import (
    get_cancel_payment_keyboard,
    get_payment_approval_keyboard,
    get_profile_actions_keyboard,
    get_confirm_delete_keyboard, 
    get_coin_packages_keyboard,
    get_cancel_keyboard_simple
)
from utils.helpers import format_profile_safe, parse_photos, user_state
from utils.translations import get_text, get_user_language  # ✅ ADD THIS IMPORT

router = Router()

# States for features
class ComplaintStates(StatesGroup):
    choosing_type = State()
    entering_details = State()

class DeleteAccountStates(StatesGroup):
    confirming = State()

class PaymentStates(StatesGroup):
    waiting_for_screenshot = State()

# ============================================================================
# PROFILE DISCOVERY COMMANDS
# ============================================================================

# Who Liked Me Command
@router.message(Command("likes"))
@router.message(Command("who_liked_me"))
@router.message(Command("likers"))
async def who_liked_me(message: Message):
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_id = message.from_user.id
    likes = db.get_user_likes(user_id)
    
    if not likes:
        await message.answer(get_text('no_likes_yet', user_lang))
        return
    
    await message.answer(get_text('likes_count', user_lang, count=len(likes)))
    
    # Show each user who liked the profile (limited to 5)
    for i, user in enumerate(likes[:5]):
        profile_text = f"{get_text('liker_number', user_lang, number=i+1)}\n\n"
        profile_text += format_profile_safe(user, user_lang)
        
        photos = parse_photos(user.get('photos', '[]'))
        
        if photos and len(photos) >= 2:
            # Send first 2 photos as media group
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
            
            await message.bot.send_media_group(
                chat_id=message.chat.id,
                media=media_group
            )
            
            # If there are more than 2 photos, mention it
            extra_photos_text = ""
            if len(photos) > 2:
                extra_photos_text = f" (+{len(photos)-2} more photos)"
            
            # Send action buttons
            await message.answer(
                get_text('someone_liked_back', user_lang, extra_photos=extra_photos_text),
                reply_markup=get_profile_actions_keyboard(user['user_id'])
            )
            
        elif photos:
            # Only one photo
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=photos[0],
                caption=profile_text,
                reply_markup=get_profile_actions_keyboard(user['user_id'])
            )
        else:
            # No photos
            await message.answer(
                profile_text,
                reply_markup=get_profile_actions_keyboard(user['user_id'])
            )

# My Matches Command
@router.message(Command("matches"))
@router.message(Command("my_matches"))
async def my_matches(message: Message):
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_id = message.from_user.id
    matches = db.get_mutual_likes(user_id)
    
    if not matches:
        await message.answer(get_text('no_matches_yet', user_lang))
        return
    
    await message.answer(get_text('matches_count', user_lang, count=len(matches)))
    
    # Show each match (limited to 5)
    for i, match in enumerate(matches[:5]):
        profile_text = f"{get_text('match_number', user_lang, number=i+1)}\n\n"
        profile_text += format_profile_safe(match, user_lang)
        
        photos = parse_photos(match.get('photos', '[]'))
        
        if photos and len(photos) >= 2:
            # Send first 2 photos as media group
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
            
            await message.bot.send_media_group(
                chat_id=message.chat.id,
                media=media_group
            )
            
            # If there are more than 2 photos, mention it
            extra_photos_text = ""
            if len(photos) > 2:
                extra_photos_text = f" (+{len(photos)-2} more photos)"
            
            # Send action buttons
            await message.answer(
                get_text('its_a_match', user_lang, extra_photos=extra_photos_text),
                reply_markup=get_profile_actions_keyboard(match['user_id'])
            )
            
        elif photos:
            # Only one photo
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=photos[0],
                caption=profile_text,
                reply_markup=get_profile_actions_keyboard(match['user_id'])
            )
        else:
            # No photos
            await message.answer(
                profile_text,
                reply_markup=get_profile_actions_keyboard(match['user_id'])
            )

# ============================================================================
# ADDITIONAL FEATURES COMMANDS
# ============================================================================

# Complain Command - Simple Number-based Menu
@router.message(Command("complain"))
@router.message(Command("report"))
async def complain_command(message: Message, state: FSMContext):
    """Handle /complain command with number-based menu"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(
        get_text('complain_prompt', user_lang),
        reply_markup=remove_keyboard
    )
    await state.set_state(ComplaintStates.choosing_type)

@router.message(ComplaintStates.choosing_type, F.text.regexp(r'^[1-8]$'))
async def handle_complaint_type_number(message: Message, state: FSMContext):
    """Handle complaint type selection by number"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    complaint_types = {
        "1": get_text('complaint_type_1', user_lang),
        "2": get_text('complaint_type_2', user_lang),
        "3": get_text('complaint_type_3', user_lang),
        "4": get_text('complaint_type_4', user_lang),
        "5": get_text('complaint_type_5', user_lang),
        "6": get_text('complaint_type_6', user_lang),
        "7": get_text('complaint_type_7', user_lang),
        "8": get_text('complaint_type_8', user_lang)
    }
    
    complaint_type = complaint_types.get(message.text)
    
    await state.update_data(complaint_type=complaint_type)
    
    await message.answer(
        get_text('complaint_type_selected', user_lang, type=complaint_type),
        reply_markup=remove_keyboard
    )
    await state.set_state(ComplaintStates.entering_details)

@router.message(ComplaintStates.choosing_type)
async def handle_invalid_complaint_number(message: Message, state: FSMContext):
    """Handle invalid number input for complaint type"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    if message.text == "/cancel":
        await state.clear()
        await message.answer(get_text('complaint_cancelled', user_lang))
        return
    
    await message.answer(get_text('invalid_complaint_number', user_lang))

@router.message(ComplaintStates.entering_details)
async def handle_complaint_details(message: Message, state: FSMContext):
    """Handle complaint details input"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    if message.text == "/cancel":
        await state.clear()
        await message.answer(get_text('complaint_cancelled', user_lang))
        return
    
    complaint_text = message.text.strip()
    
    if len(complaint_text) < 10:
        await message.answer(get_text('complaint_too_short', user_lang))
        return
    
    if len(complaint_text) > 500:
        await message.answer(get_text('complaint_too_long', user_lang))
        return
    
    user_data = await state.get_data()
    complaint_type = user_data.get('complaint_type')
    
    # Save complaint to database
    success = db.add_complaint(
        user_id=message.from_user.id,
        complaint_type=complaint_type,
        complaint_text=complaint_text
    )
    
    if success:
        # Notify admin (keep in English for admin)
        user_info = db.get_user(message.from_user.id)
        username = f"@{user_info['username']}" if user_info.get('username') else "No username"
        
        admin_message = get_text('admin_complaint_notification', 'english',
                               first_name=user_info['first_name'],
                               user_id=message.from_user.id,
                               username=username,
                               type=complaint_type,
                               text=complaint_text,
                               time=message.date.strftime('%Y-%m-%d %H:%M:%S'))
        
        try:
            if config.ADMIN_ID:
                await message.bot.send_message(config.ADMIN_ID, admin_message)
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        await message.answer(get_text('complaint_submitted', user_lang))
    else:
        await message.answer(get_text('complaint_failed', user_lang))
    
    await state.clear()

# Language Command
@router.message(Command("language"))
@router.message(Command("lang"))
async def language_command(message: Message):
    """Handle /language command with reply buttons"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_data = db.get_user(message.from_user.id)
    current_language = user_data.get('language', 'english') if user_data else 'english'
    
    language_names = {
        'english': get_text('language_english', user_lang),
        'amharic': get_text('language_amharic', user_lang),
        'oromo': get_text('language_oromo', user_lang)
    }
    
    current_lang_name = language_names.get(current_language, 'English')
    
    await message.answer(
        get_text('language_settings', user_lang, current_lang=current_lang_name),
        reply_markup=get_language_keyboard()
    )

@router.message(F.text.in_(["🇬🇧 English", "🇪🇹 Amharic", "🇪🇹 Affan Oromo"]))
async def handle_language_selection_reply(message: Message):
    """Handle language selection from reply buttons"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    language_map = {
        "🇬🇧 English": "english",
        "🇪🇹 Amharic": "amharic", 
        "🇪🇹 Affan Oromo": "oromo"
    }
    
    language_code = language_map.get(message.text)
    if not language_code:
        return
    
    # Update user language in database
    success = db.update_user_language(message.from_user.id, language_code)
    
    if success:
        language_names = {
            'english': get_text('language_english', user_lang),
            'amharic': get_text('language_amharic', user_lang),
            'oromo': get_text('language_oromo', user_lang)
        }
        language_name = language_names[language_code]
        
        await message.answer(
            get_text('language_updated', user_lang, language=language_name),
            reply_markup=remove_keyboard
        )
    else:
        await message.answer(
            get_text('language_update_failed', user_lang),
            reply_markup=remove_keyboard
        )

# Buy Coins Command
@router.message(Command("buycoins"))
@router.message(Command("coins"))
@router.message(Command("premium"))
async def buy_coins_command(message: Message):
    """Handle /buycoins command"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(
        get_text('buy_coins', user_lang),
        reply_markup=get_coin_packages_keyboard()
    )

@router.callback_query(F.data.startswith("coins_"))
async def handle_coin_selection(callback: CallbackQuery, state: FSMContext):
    """Handle coin package selection and request payment screenshot"""
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    package_map = {
        "coins_100": {"coins": 100, "price": 4.99, "name": "100 Coins"},
        "coins_250": {"coins": 250, "price": 9.99, "name": "250 Coins"}, 
        "coins_500": {"coins": 500, "price": 17.99, "name": "500 Coins"},
        "coins_1000": {"coins": 1000, "price": 29.99, "name": "1000 Coins"},
        "coins_2500": {"coins": 2500, "price": 69.99, "name": "2500 Coins"}
    }
    
    package = package_map.get(callback.data)
    if not package:
        await callback.answer("Invalid package selection")
        return
    
    coins = package["coins"]
    price = package["price"]
    package_name = package["name"]
    
    # Store package info in state
    await state.update_data(
        selected_package=package_name,
        coins_amount=coins,
        price=price
    )
    
    await callback.message.edit_text(
        get_text('package_selected', user_lang, package=package_name, coins=coins, price=price),
        reply_markup=get_cancel_payment_keyboard()
    )
    
    await state.set_state(PaymentStates.waiting_for_screenshot)
    await callback.answer()

# Admin Command to Add Coins to Users
@router.message(Command("addcoin"))
async def add_coins_admin(message: Message):
    """Admin command to add coins to users"""
    # Check if user is admin
    if message.from_user.id != config.ADMIN_ID:
        await message.answer(get_text('admin_only', 'english'))
        return
    
    try:
        # Command format: /addcoins <user_id> <coin_amount> [reason]
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer(get_text('addcoins_usage', 'english'))
            return
        
        user_id = int(parts[1])
        coin_amount = int(parts[2])
        reason = " ".join(parts[3:]) if len(parts) > 3 else "Admin added coins for you."
        
        # Check if user exists
        user_data = db.get_user(user_id)
        if not user_data:
            await message.answer(get_text('user_not_found', 'english'))
            return
        
        success = db.add_user_coins(user_id, coin_amount)
        
        if success:
            new_balance = db.get_user_coins(user_id)
            await message.answer(
                get_text('coins_added_success', 'english',
                        first_name=user_data['first_name'],
                        user_id=user_id,
                        amount=coin_amount,
                        balance=new_balance,
                        reason=reason)
            )
            
            # Notify user in their language
            user_lang = get_user_language(user_id, db)
            try:
                await message.bot.send_message(
                    chat_id=user_id,
                    text=get_text('coins_added_user_notification', user_lang,
                                 amount=coin_amount,
                                 balance=new_balance,
                                 reason=reason)
                )
            except Exception as e:
                await message.answer(f"✅ Coins added but failed to notify user: {e}")
        else:
            await message.answer(get_text('coins_added_failed', 'english'))
            
    except ValueError:
        await message.answer(get_text('invalid_user_id', 'english'))
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(PaymentStates.waiting_for_screenshot, F.photo)
async def handle_payment_screenshot(message: Message, state: FSMContext):
    """Handle payment screenshot submission"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_data = await state.get_data()
    
    # Get the highest quality photo (screenshot)
    screenshot_file_id = message.photo[-1].file_id
    
    # Store payment request in database
    payment_id = db.add_payment_request(
        user_id=message.from_user.id,
        package_name=user_data['selected_package'],
        coins_amount=user_data['coins_amount'],
        price=user_data['price'],
        screenshot_file_id=screenshot_file_id
    )
    
    if payment_id == -1:
        await message.answer(get_text('complaint_failed', user_lang))  # Reuse error message
        await state.clear()
        return
    
    # Get user info for admin notification
    user_info = db.get_user(message.from_user.id)
    username = f"@{user_info['username']}" if user_info.get('username') else "No username"
    
    # Prepare admin notification (in English)
    admin_caption = (
        "💰 New Payment Request\n\n"
        f"User: {user_info['first_name']} (ID: {message.from_user.id})\n"
        f"Username: {username}\n"
        f"Package: {user_data['selected_package']}\n"
        f"Amount: ${user_data['price']}\n"
        f"Coins: {user_data['coins_amount']}\n"
        f"Payment ID: #{payment_id}\n\n"
        f"Time: {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "Please verify the payment and approve or reject."
    )
    
    # Forward screenshot to admin with approval buttons
    try:
        if config.ADMIN_ID:
            await message.bot.send_photo(
                chat_id=config.ADMIN_ID,
                photo=screenshot_file_id,
                caption=admin_caption,
                reply_markup=get_payment_approval_keyboard(payment_id)
            )
    except Exception as e:
        print(f"Failed to notify admin: {e}")
        await message.answer(get_text('complaint_failed', user_lang))  # Reuse error message
        await state.clear()
        return
    
    await message.answer(get_text('payment_screenshot_received', user_lang))
    await state.clear()

@router.message(PaymentStates.waiting_for_screenshot)
async def handle_invalid_screenshot(message: Message):
    """Handle non-photo messages during screenshot submission"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(get_text('invalid_screenshot', user_lang))

# Payment approval handlers (keep admin messages in English)
@router.callback_query(F.data.startswith("approve_payment_"))
async def approve_payment(callback: CallbackQuery):
    """Admin approves a payment"""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer(get_text('admin_only', 'english'))
        return
    
    payment_id = int(callback.data.split("_")[2])
    payment = db.get_payment_request(payment_id)
    
    if not payment:
        await callback.answer(get_text('user_not_found', 'english'))
        return
    
    if payment['status'] == 'approved':
        await callback.answer(f"⚠️ Payment #{payment_id} was already approved on {payment.get('processed_at', 'previous time')}.")
        return
    elif payment['status'] == 'rejected':
        await callback.answer(f"⚠️ Payment #{payment_id} was rejected and cannot be approved.")
        return
    elif payment['status'] != 'pending':
        await callback.answer(f"⚠️ Payment #{payment_id} has unexpected status: {payment['status']}")
        return
    
    try:
        # Add coins to user
        success = db.add_user_coins(payment['user_id'], payment['coins_amount'])
        
        if success:
            # Update payment status
            db.update_payment_status(payment_id, 'approved', callback.from_user.id, "Payment verified and approved")
            
            # Notify user in their language
            user_lang = get_user_language(payment['user_id'], db)
            try:
                await callback.bot.send_message(
                    chat_id=payment['user_id'],
                    text=get_text('payment_approved_user', user_lang,
                                 amount=payment['coins_amount'],
                                 balance=db.get_user_coins(payment['user_id']))
                )
            except Exception as e:
                print(f"Failed to notify user: {e}")
            
            await callback.message.edit_caption(
                caption=f"✅ Payment Approved\n\n{callback.message.caption}\n\nApproved by: {callback.from_user.id}",
                reply_markup=None
            )
            await callback.answer(f"✅ Approved payment #{payment_id}")
        else:
            await callback.answer(get_text('coins_added_failed', 'english'))
    except Exception as e:
        db.update_payment_status(payment_id, 'pending', None, f"Error during processing: {str(e)}")
        await callback.answer("❌ Error processing payment. Please try again.")
        print(f"Payment approval error: {e}")

@router.callback_query(F.data.startswith("reject_payment_"))
async def reject_payment(callback: CallbackQuery):
    """Admin rejects a payment"""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer(get_text('admin_only', 'english'))
        return
    
    payment_id = int(callback.data.split("_")[2])
    payment = db.get_payment_request(payment_id)
    
    if not payment:
        await callback.answer(get_text('user_not_found', 'english'))
        return
    
    # Update payment status
    db.update_payment_status(payment_id, 'rejected', callback.from_user.id, "Payment rejected by admin")
    
    # Notify user in their language
    user_lang = get_user_language(payment['user_id'], db)
    try:
        await callback.bot.send_message(
            chat_id=payment['user_id'],
            text=get_text('payment_rejected_user', user_lang)
        )
    except Exception as e:
        print(f"Failed to notify user: {e}")
    
    await callback.message.edit_caption(
        caption=f"❌ Payment Rejected\n\n{callback.message.caption}\n\nRejected by: {callback.from_user.id}",
        reply_markup=None
    )
    await callback.answer(f"❌ Rejected payment #{payment_id}")

@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    """Cancel payment process"""
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await state.clear()
    await callback.message.edit_text(
        get_text('payment_cancelled', user_lang),
        reply_markup=None
    )
    await callback.answer()

# Admin command to view pending payments (keep in English)
@router.message(Command("pending_payments"))
async def view_pending_payments(message: Message):
    """Admin command to view pending payments"""
    if message.from_user.id != config.ADMIN_ID:
        await message.answer(get_text('admin_only', 'english'))
        return
    
    pending_payments = db.get_pending_payments()
    
    if not pending_payments:
        await message.answer(get_text('no_pending_payments', 'english'))
        return
    
    await message.answer(get_text('pending_payments_count', 'english', count=len(pending_payments)))
    
    for payment in pending_payments:
        payment_info = get_text('payment_info', 'english',
                              id=payment['id'],
                              first_name=payment['first_name'],
                              user_id=payment['user_id'],
                              username=payment['username'],
                              package=payment['package_name'],
                              price=payment['price'],
                              coins=payment['coins_amount'],
                              time=payment['created_at'])
        
        await message.answer(
            payment_info,
            reply_markup=get_payment_approval_keyboard(payment['id'])
        )

# Delete Account Command
@router.message(Command("deleteaccount"))
@router.message(Command("delete"))
@router.message(Command("removeaccount"))
async def delete_account_command(message: Message, state: FSMContext):
    """Handle /deleteaccount command"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(
        get_text('delete_account_warning', user_lang),
        reply_markup=get_confirm_delete_keyboard()
    )
    await state.set_state(DeleteAccountStates.confirming)

@router.callback_query(DeleteAccountStates.confirming, F.data == "confirm_delete_yes")
async def confirm_delete_yes(callback: CallbackQuery, state: FSMContext):
    """Handle account deletion confirmation"""
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    user_id = callback.from_user.id
    
    # Delete user account
    success = db.delete_user_account(user_id)
    
    if success:
        await callback.message.edit_text(
            get_text('account_deleted_success', user_lang),
            reply_markup=None
        )
        
        # Notify admin (in English)
        try:
            if config.ADMIN_ID:
                await callback.bot.send_message(
                    config.ADMIN_ID,
                    get_text('admin_account_deleted', 'english', user_id=user_id)
                )
        except Exception as e:
            print(f"Failed to notify admin: {e}")
            
    else:
        await callback.message.edit_text(
            get_text('account_deleted_failed', user_lang),
            reply_markup=None
        )
    
    await state.clear()
    await callback.answer()

@router.callback_query(DeleteAccountStates.confirming, F.data == "confirm_delete_no")
async def confirm_delete_no(callback: CallbackQuery, state: FSMContext):
    """Handle account deletion cancellation"""
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await callback.message.edit_text(
        get_text('account_deletion_cancelled', user_lang),
    )
    await state.clear()
    await callback.answer()

# ============================================================================
# UTILITY COMMANDS
# ============================================================================

# Cancel handler for any state
@router.message(Command("cancel"))
async def cancel_operation(message: Message, state: FSMContext):
    """Cancel any ongoing operation"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(get_text('no_operation_cancel', user_lang))
        return
    
    await state.clear()
    user_state.clear_state(message.from_user.id)
    await message.answer(get_text('operation_cancelled', user_lang))

# Cancel handlers for inline operations
@router.callback_query(F.data == "cancel_operation")
async def cancel_inline_operation(callback: CallbackQuery, state: FSMContext):
    """Cancel any ongoing operation from inline button"""
    user_lang = get_user_language(callback.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await state.clear()
    await callback.message.edit_text(
        get_text('inline_operation_cancelled', user_lang),
    )
    await callback.answer()

# Help Command
@router.message(Command("help"))
async def help_command(message: Message):
    """Show help message with all commands"""
    user_lang = get_user_language(message.from_user.id, db)  # ✅ GET USER LANGUAGE
    
    await message.answer(get_text('help_text', user_lang))