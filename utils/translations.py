# utils/translations.py
def get_user_language(user_id: int, db) -> str:
    """Get user's preferred language from database"""
    user_data = db.get_user(user_id)
    return user_data.get('language', 'english') if user_data else 'english'

def get_text(key: str, language: str = 'english', **kwargs) -> str:
    """Get translated text for a given key and language"""
    translations = {
        'english': {
            # Registration flow
            'welcome': "👋 Welcome to Ethiopia Connect!",
            'choose_language': "Please choose your preferred language:",
            'enter_name': "Great! Now please enter your full name:",
            'share_contact': "📞 Please share your contact:",
            'enter_age': "📅 How old are you? (Please enter your age):",
            'choose_gender': "👤 Please choose your gender:",
            'choose_religion': "🙏 Please choose your religion:",
            'share_location': "📍 Please share your location or choose a city:",
            'choose_city': "🏙️ Please choose your city:",
            'enter_bio': "📝 Please tell us a little about yourself:",
            'share_photos': "📸 Send your photos (at least 2 recommended):",
            'photo_received': "✅ Photo {count} received! Send more or type /done",
            'registration_complete': "✅ Registration completed! 🎉",
            
            # Main menu
            'find_matches': "🔍 Find Matches",
            'my_profile': "👤 My Profile", 
            'my_messages': "💌 My Messages",
            
            # Matching
            'no_matches': "😔 No profiles found. Check back later!",
            'all_profiles_seen': "🎉 You've seen all profiles!",
            'nice_profile': "🔥 Nice profile! Ready to make a move?",
            'like': "❤️ Like",
            'message': "💌 Message",
            'skip': "⏭️ Skip",
            
            # Profile commands
            'no_likes': "😔 No one liked you yet.",
            'likes_count': "❤️ {count} people liked you!",
            'no_matches_cmd': "💔 No matches yet.",
            'matches_count': "💕 You have {count} matches!",
            
            # Other features
            'complaint_success': "✅ Complaint submitted!",
            'language_updated': "✅ Language updated to {language}",
            'screenshot_received': "✅ Payment received! Under review.",
            'account_deleted': "✅ Account deleted!",
            'cancel': "❌ Cancel",
            'registration_start': "Please choose your preferred language:",
            'name_prompt': "Great! Now please enter your full name:",
            'invalid_name': "Please enter a valid name (at least 2 characters):",
            'contact_prompt': "Please share your contact using the button below:",
            'share_contact_button': "📱 Share Contact",
            'age_prompt': "How old are you? (Please enter your age):",
            'invalid_age_range': "Please enter a valid age between {min_age} and {max_age}:",
            'invalid_age_number': "Please enter a valid number for your age:",
            'gender_prompt': "Please choose your gender:",
            'religion_prompt': "Please choose your religion:",
            'location_prompt': "Please share your location or choose a city:",
            'city_choice_prompt': "Please choose your city from the list below:",
            'bio_prompt': "Please tell us a little about yourself (your interests, hobbies, etc.):",
            'photos_prompt': "Please upload at least two clear photos of yourself",
            'duplicate_photo': "You already uploaded this photo. Please upload a different one.",
            'photo_added': "Photo added to your profile!",
            'photos_save_error': "Error saving your photos. Please try uploading again.",
            'registration_success': "You can now start finding matches and connecting with people.",
            
            # Admin notifications (keep in English)
            'admin_new_user': "🆕 New user started the bot:\n👤 Name: {first_name} {last_name}\n🆔 ID: {user_id}\n📱 Username: {username}",
            'no_username': "No username",
            'incomplete_registration': "Please complete your registration first using /start",
            'no_photos_profile': "Please complete your profile and add photos first to start browsing.",
            'incomplete_profile': "Please complete your profile setup first.",
            'fetching_matches': "🔄 Fetching fresh matches for you...",
            'no_fresh_matches': "😔 No new profiles available yet. Check back later!",
            'profile_setup_required': "❌ Please complete your profile setup.",
            'like_sent': "❤️ Like sent!",
            'already_liked': "You already liked this profile!",
            'skipped': "⏭️ Skipped",
            'user_not_found': "User not found",
            'write_message_to': "💌 Write a message to {first_name}:",
            'error_try_again': "Error: Please try again.",
            'message_sent': "✅ Message sent!",
            'message_delivery_failed': "❌ Could not deliver message. User might have blocked the bot.",
            'message_send_error': "❌ Error sending message. Please try again.",
            'write_reply_to': "💌 Write a reply to {first_name}:",
            'profile_not_found': "Profile not found",
            'total_photos': "You have {count} photos in total.",
            'profile_error': "Error showing profile",
            'user_blocked': "🚫 User blocked",
            'block_success': "User has been blocked. You won't see their profile anymore.",
            'block_error': "❌ Error blocking user",
            'cancelled': "❌ Cancelled",
            
            # Profile display texts
            'profile_display_error': "Error displaying profile. Please try again.",
            'unknown_user': "User",
            
            # Additional matching texts
            'all_profiles_seen': "🎉 You've seen all available profiles!\nCheck back later for new matches.",
            'no_matches_found': "😔 No new profiles found at the moment.\nCheck back later for new matches!",
            'action_prompt': "🔥 Nice profile! Ready to make a move?",
            'no_likes_yet': "No one has liked your profile yet.\nKeep browsing to get more visibility!",
            'likes_count': "{count} people liked your profile!\n\nUse /browse to like them back and create matches!",
            'liker_number': "Liker #{number}",
            'someone_liked_back': "🔥 Someone liked you back{extra_photos}! Interested?",
            'no_matches_yet': "You don't have any matches yet.\nStart liking profiles with /browse to get matches!",
            'matches_count': "💕 You have {count} matches!\n\nHere are your mutual matches:",
            'match_number': "Match #{number}",
            'its_a_match': "💕 It's a match{extra_photos}! Start the conversation?",
            
            # Complaint system
            'complain_prompt': "📝 File a Complaint\n\nSelect a reason by sending its number:\n\n1. Inappropriate Photos\n2. Harassment or Bullying\n3. Fake Profile\n4. Spam\n5. Bug/Technical Issue\n6. Payment/Subscription Issue\n7. Feature Request\n8. Other\n\nType the number (1-8) and send it:\nOr type /cancel to cancel",
            'complaint_type_selected': "📝 Complaint Type: {type}\n\nPlease describe your complaint in detail (max 500 characters):\n\nType your complaint below:\nOr type /cancel to cancel",
            'invalid_complaint_number': "Please enter a valid number between 1-8:",
            'complaint_cancelled': "✅ Complaint cancelled.",
            'complaint_too_short': "Please provide more details (at least 10 characters).",
            'complaint_too_long': "Complaint is too long. Maximum 500 characters allowed.",
            'complaint_submitted': "✅ Complaint Submitted Successfully!\n\nThank you for your feedback. Our team will review your complaint and take appropriate action.\n\nWe appreciate you helping us improve the community!",
            'complaint_failed': "Failed to submit complaint. Please try again later.",
            'admin_complaint_notification': "🚨 New Complaint Received\n\nUser: {first_name} (ID: {user_id})\nUsername: {username}\nType: {type}\nComplaint: {text}\n\nTime: {time}",
            
            # Language settings
            'language_settings': "🌐 Language Settings\n\nCurrent language: {current_lang}\n\nSelect your preferred language:",
            'language_updated': "✅ Language Updated!\n\nYour language has been set to: {language}\n\nThe bot will now use this language for all interactions.",
            'language_update_failed': "Failed to update language. Please try again.",
            
            # Coin system
            'buy_coins': "💰 Buy Coins",
            'package_selected': "🛒 Package Selected: {package}\n\n{coins} Coins - ${price}\n\n💰 Payment Instructions:\n1. Send ${price} via:\n   • 💳 Credit Card\n   • 📱 Mobile Payment\n   • 🌐 Online Transfer\n\n2. Take a screenshot of your payment confirmation\n3. Send the screenshot here\n\nAfter verification, coins will be added to your account within 24 hours.",
            'payment_screenshot_received': "✅ Payment Screenshot Received!\n\nYour payment is under review. We'll notify you once it's processed.\n\n⏳ Processing Time: Usually within 24 hours\n📞 Support: Contact @admin if you have questions",
            'invalid_screenshot': "Please send a screenshot of your payment confirmation.\n\nIf you're having trouble, please contact @admin for assistance.",
            'payment_cancelled': "❌ Payment process cancelled.",
            
            # Admin commands
            'admin_only': "❌ Admin only command.",
            'addcoins_usage': "Usage: /addcoins <user_id> <coin_amount> [reason]",
            'user_not_found': "❌ User not found.",
            'coins_added_success': "✅ Coins Added Successfully!\n\nUser: {first_name} (ID: {user_id})\nCoins Added: {amount}\nNew Balance: {balance} coins\nReason: {reason}",
            'coins_added_failed': "❌ Failed to add coins.",
            'invalid_user_id': "❌ Invalid user ID or coin amount. Usage: /addcoins <user_id> <coin_amount> [reason]",
            'coins_added_user_notification': "🎉 Coins Added to Your Account!\n\n{amount} coins have been added to your account.\n\n💰 New Balance: {balance} coins\n\nReason: {reason}",
            'payment_approved_user': "🎉 Payment Approved!\n\n{amount} coins have been added to your account!\n\n💰 New Balance: {balance} coins\n\nThank you for your purchase! 🎊",
            'payment_rejected_user': "❌ Payment Rejected\n\nYour payment was rejected. Please contact @admin for more information.\n\nIf you believe this is an error, please provide your transaction details to support.",
            'no_pending_payments': "✅ No pending payments.",
            'pending_payments_count': "📋 Pending Payments: {count}",
            'payment_info': "Payment ID: #{id}\nUser: {first_name} (ID: {user_id})\nUsername: @{username}\nPackage: {package}\nAmount: ${price}\nCoins: {coins}\nTime: {time}\n\nUse /addcoins {user_id} {coins} to manually add coins",
            
            # Account deletion
            'delete_account_warning': "🚨 Delete Account\n\n⚠️ This action is permanent and cannot be undone!\n\nWhat will be deleted:\n• Your profile information\n• All your photos\n• Your matches and likes\n• Your messages\n• Your account data\n\nAre you sure you want to delete your account?",
            'account_deleted_success': "✅ Account Deleted Successfully\n\nYour account and all associated data have been permanently deleted.\n\nWe're sorry to see you go! If you change your mind, you can always create a new account with /start.\n\nThank you for being part of our community! 👋",
            'account_deleted_failed': "❌ Failed to Delete Account\n\nThere was an error deleting your account. Please try again later or contact support.",
            'account_deletion_cancelled': "✅ Account Deletion Cancelled\n\nYour account has NOT been deleted.\n\nWe're glad you decided to stay! 😊",
            'admin_account_deleted': "🗑️ User {user_id} deleted their account.",
            
            # Utility commands
            'no_operation_cancel': "No active operation to cancel.",
            'operation_cancelled': "✅ Operation cancelled.",
            'inline_operation_cancelled': "❌ Operation cancelled.",
            
            # Help command
            'help_text': """
🤖 Ethiopia Connect Bot - Commands Guide

🔍 Discovery & Matching:
• `/browse` - Discover new profiles
• `/likes` - See who liked your profile  
• `/matches` - See your mutual matches

👤 Profile Management:
• `/profile` - View your profile
• `/language` - Change bot language

💰 Premium Features:
• `/buycoins` - Purchase coins for premium features

🛡️ Safety & Support:
• `/complain` - Report issues or send feedback
• `/deleteaccount` - Permanently delete your account

💌 Messaging:
• Use the inline buttons when browsing profiles to message users

🛠 Utility Commands:
• `/help` - Show this help message
• `/cancel` - Cancel current operation

💡 Tip: Use the menu buttons for quick access to main features!
            """,
            
            # Complaint types (for dynamic use)
            'complaint_type_1': "Inappropriate Photos",
            'complaint_type_2': "Harassment or Bullying", 
            'complaint_type_3': "Fake Profile",
            'complaint_type_4': "Spam",
            'complaint_type_5': "Bug/Technical Issue",
            'complaint_type_6': "Payment/Subscription Issue",
            'complaint_type_7': "Feature Request",
            'complaint_type_8': "Other",
            
            # Language names
            'language_english': "🇬🇧 English",
            'language_amharic': "🇪🇹 Amharic",
            'language_oromo': "🇪🇹 Affan Oromo",
            'language_tigrigna': "🇪🇹 Tigrinya",
            'incomplete_profile_registration': "Please complete your registration first using /start",
            'total_photos_count': "You have {count} photos in total.",
            'messages_empty': "📨 Your messages will appear here when you receive them.\nStart browsing profiles to connect with people!",
            'profile_unknown': "Unknown",
            'profile_language': "🗣️ {profile_language}  |  🌍 {city}",
            'profile_city_not_specified': "Not specified",
            'profile_religion_not_specified': "Not specified",
            'profile_balance': "💰 Balance: {coins} coin(s)",
            
            # Stats formatting (keep emojis as requested)
            'profile_stats': "❤️ Likes: {likes}   🤝 Matches: {matches}",
            
            # Lists formatting
            'no_likes_yet_list': "No likes yet.",
            'likes_list_header': "❤️ Users who liked your profile:\n\n",
            'no_matches_yet_list': "No matches yet.", 
            'matches_list_header': "💕 Your mutual matches:\n\n",

            # Errors
            'error': "❌ Error",
            'try_again': "Please try again.",
        },
        
        'amharic': {
            # Registration flow
            'welcome': "👋 እንኳን ወደ ኢትዮጵያ ኮንንት በደህና መጡ!",
            'choose_language': "እባክዎ የሚፈልጉትን ቋንቋ ይምረጡ:",
            'enter_name': "ጥሩ! አሁን ሙሉ ስምዎን ያስገቡ:",
            'share_contact': "📞 ስልክ ቁጥርዎን ያጋሩ:",
            'enter_age': "📅 ዕድሜዎ ስንት ነው?",
            'choose_gender': "👤 ጾታዎን ይምረጡ:",
            'choose_religion': "🙏 ሃይማኖትዎን ይምረጡ:",
            'share_location': "📍 ከተማዎን ያጋሩ:",
            'choose_city': "🏙️ ከተማ ይምረጡ:",
            'enter_bio': "📝 ስለ ራስዎ ይንገሩን:",
            'share_photos': "📸 ፎቶዎችዎን ይላኩ (ቢያንስ 2 ይመከራል):",
            'photo_received': "✅ ፎቶ {count} ተቀብሏል! ተጨማሪ ይላኩ ወይም /done ይበሉ",
            'registration_complete': "✅ ምዝገባ ተጠናቅቋል! 🎉",
            
            # Main menu
            'find_matches': "🔍 ማጣጣሚያዎችን ፈልግ",
            'my_profile': "👤 የእኔ መገለጫ", 
            'my_messages': "💌 መልዕክቶቼ",
            
            # Matching
            'no_matches': "😔 ምንም መገለጫ አልተገኘም። ቆይተው ይመልከቱ!",
            'all_profiles_seen': "🎉 ሁሉንም መገለጫዎች አይተዋል!",
            'nice_profile': "🔥 ጥሩ መገለጫ! ለመስራት ዝግጁ ነዎት?",
            'like': "❤️ አብዝተህ",
            'message': "💌 መልዕክት",
            'skip': "⏭️ አልፍ",
            
            # Profile commands
            'no_likes': "😔 እስካሁን ማንም አላብዝቶህም።",
            'likes_count': "❤️ {count} ሰዎች አብዝተውሃል!",
            'no_matches_cmd': "💔 እስካሁን ማጣጣሚያ የሎትም።",
            'matches_count': "💕 {count} ማጣጣሚያዎች አሎት!",
            
            # Other features
            'complaint_success': "✅ ቅሬታዎ ቀርቧል!",
            'language_updated': "✅ ቋንቋዎ ወደ {language} ተቀይሯል",
            'screenshot_received': "✅ ክፍያዎ ተቀብሏል! በግምገማ ላይ።",
            'account_deleted': "✅ መለያዎ ተሰርዟል!",
            'cancel': "❌ ሰርዝ",
            'registration_start': "እባክዎ የሚፈልጉትን ቋንቋ ይምረጡ:",
            'name_prompt': "ጥሩ! አሁን ሙሉ ስምዎን ያስገቡ:",
            'invalid_name': "እባክዎ ትክክለኛ ስም ያስገቡ (ቢያንስ 2 ፊደላት):",
            'contact_prompt': "እባክዎ ከታች ያለውን ቁልፍ በመጠቀም ስልክ ቁጥርዎን ያጋሩ:",
            'share_contact_button': "📱 ስልክ ቁጥር ያጋሩ",
            'age_prompt': "ዕድሜዎ ስንት ነው? (እባክዎ ዕድሜዎን ያስገቡ):",
            'invalid_age_range': "እባክዎ ትክክለኛ ዕድሜ ከ{min_age} እስከ {max_age} ያስገቡ:",
            'invalid_age_number': "እባክዎ ለዕድሜዎ ትክክለኛ ቁጥር ያስገቡ:",
            'gender_prompt': "እባክዎ ጾታዎን ይምረጡ:",
            'religion_prompt': "እባክዎ ሃይማኖትዎን ይምረጡ:",
            'location_prompt': "እባክዎ ከተማዎን ያጋሩ ወይም ከተማ ይምረጡ:",
            'city_choice_prompt': "እባክዎ ከታች ካለው ዝርዝር ከተማዎን ይምረጡ:",
            'bio_prompt': "እባክዎ ስለ ራስዎ ትንሽ ይንገሩን (ፍላጎቶችዎ፣ የግዴታ እንቅስቃሴዎችዎ፣ ወዘተ.):",
            'photos_prompt': "እባክዎ ቢያንስ ሁለት ግልጽ የሆኑ ፎቶዎችዎን ይስቀሉ",
            'duplicate_photo': "ይህን ፎቶ አስቀድመው ሰቅለዋል። እባክዎ ሌላ ፎቶ ይስቀሉ።",
            'photo_added': "ፎቶው ወደ መገለጫዎ ተጨምሯል!",
            'photos_save_error': "ፎቶዎችዎን ማስቀመጥ አልተቻለም። እባክዎ እንደገና ይሞክሩ።",
            'registration_success': "አሁን ማጣጣሚያዎችን ማግኘት እና ሰዎችን መገናኘት ይችላሉ።",
            'incomplete_registration': "እባክዎ መጀመሪያ ምዝገባዎን በ /start ይጨርሱ",
            'no_photos_profile': "እባክዎ መጀመሪያ መገለጫዎን ይጨርሱ እና ፎቶዎችዎን ይጨምሩ",
            'incomplete_profile': "እባክዎ መጀመሪያ መገለጫዎን ያጠናቅቁ",
            'fetching_matches': "🔄 አዳዲስ ማጣጣሚያዎች ለእርስዎ በማግኘት ላይ...",
            'no_fresh_matches': "😔 አዳዲስ መገለጫዎች አሁንም የሉም። ቆይተው ይመልከቱ!",
            'profile_setup_required': "❌ እባክዎ መገለጫዎን ያጠናቅቁ",
            'like_sent': "❤️ አብዝተህ!",
            'already_liked': "ይህን መገለጫ አስቀድመው አብዝተውታል!",
            'skipped': "⏭️ አልፍ",
            'user_not_found': "ተጠቃሚ አልተገኘም",
            'write_message_to': "💌 ለ {first_name} መልዕክት ይጻፉ:",
            'error_try_again': "ስህተት፡ እባክዎ እንደገና ይሞክሩ",
            'message_sent': "✅ መልዕክቱ ተልኳል!",
            'message_delivery_failed': "❌ መልዕክቱ ሊደርስ አልቻለም። ተጠቃሚው ቦቱን ሊከለክል ይችላል።",
            'message_send_error': "❌ መልዕክት ለመላክ ስህተት። እባክዎ እንደገና ይሞክሩ።",
            'write_reply_to': "💌 ለ {first_name} መልስ ይጻፉ:",
            'profile_not_found': "መገለጫ አልተገኘም",
            'total_photos': "{count} ፎቶዎች አሎት።",
            'profile_error': "መገለጫ ማሳየት አልተቻለም",
            'user_blocked': "🚫 ተጠቃሚ ታግዷል",
            'block_success': "ተጠቃሚው ታግዷል። መገለጫውን ከአሁን በኋላ አታይም።",
            'block_error': "❌ ተጠቃሚን ለማገድ ስህተት",
            'cancelled': "❌ ተሰርዟል",
            
            # Profile display texts
            'profile_display_error': "መገለጫ ማሳየት አልተቻለም። እባክዎ እንደገና ይሞክሩ።",
            'unknown_user': "ተጠቃሚ",
            
            # Additional matching texts
            'all_profiles_seen': "🎉 ሁሉንም የሚገኙ መገለጫዎች አይተዋል!\nለአዳዲስ ማጣጣሚያዎች ቆይተው ይመልከቱ።",
            'no_matches_found': "😔 በአሁኑ ጊዜ ምንም አዳዲስ መገለጫዎች አልተገኙም።\nቆይተው ይመልከቱ!",
            'action_prompt': "🔥 ጥሩ መገለጫ! ለመስራት ዝግጁ ነዎት?",
            'no_likes_yet': "እስካሁን ማንም መገለጫዎን አላብዝተም።\nተጨማሪ እይታ ለማግኘት መሰረም ይቀጥሉ!",
            'likes_count': "{count} ሰዎች መገለጫዎን አብዝተዋል!\n\nእነሱን ለማብዛት እና ማጣጣሚያዎችን ለመፍጠር /browse ይጠቀሙ!",
            'liker_number': "አብዝተኛ #{number}",
            'someone_liked_back': "🔥 ማንም አብዝቶሃል{extra_photos}! ፍላጎት አሎት?",
            'no_matches_yet': "እስካሁን ምንም ማጣጣሚያዎች የሎትም።\nማጣጣሚያዎችን ለማግኘት መገለጫዎችን በ /browse ይምረጡ!",
            'matches_count': "💕 {count} ማጣጣሚያዎች አሎት!\n\nእነዚህ የእርስዎ የጋራ ማጣጣሚያዎች ናቸው፡",
            'match_number': "ማጣጣሚያ #{number}",
            'its_a_match': "💕 ማጣጣሚያ ነው{extra_photos}! ውይይቱን መጀመር ይፈልጋሉ?",
            
            # Complaint system
            'complain_prompt': "📝 ቅሬታ ለመግባት\n\nቁጥሩን በመላክ ምክንያት ይምረጡ፡\n\n1. ተገቢ ያልሆኑ ፎቶዎች\n2. አሰታውቅ ወይም ማጭበርበር\n3. ሐሰተኛ መገለጫ\n4. ስፓም\n5. ስህተት/ቴክኒካል ችግር\n6. ክፍያ/የደንበኝነት ችግር\n7. የባህሪ ጥያቄ\n8. ሌላ\n\nቁጥሩን ይተይቡ እና ይላኩ (1-8)፡\nወይም ለማቆም /cancel ይተይቡ",
            'complaint_type_selected': "📝 የቅሬታ አይነት፡ {type}\n\nእባክዎ ቅሬታዎን በዝርዝር ይግለጹ (ከፍተኛ 500 ፊደላት)፡\n\nቅሬታዎን ከታች ይተይቡ፡\nወይም ለማቆም /cancel ይተይቡ",
            'invalid_complaint_number': "እባክዎ ትክክለኛ ቁጥር ከ1-8 ያስገቡ፡",
            'complaint_cancelled': "✅ ቅሬታ ተሰርዟል።",
            'complaint_too_short': "እባክዎ ተጨማሪ ዝርዝሮችን ያቅርቡ (ቢያንስ 10 ፊደላት)።",
            'complaint_too_long': "ቅሬታው በጣም ረጅም ነው። ከፍተኛው 500 ፊደላት ብቻ ይፈቀዳሉ።",
            'complaint_submitted': "✅ ቅሬታዎ በተሳካ ሁኔታ ቀርቧል!\n\nለግብዣዎ እናመሰግናለን። ቡድናችን ቅሬታዎን ይገመግማል እና ተገቢውን እርምጃ ይወስዳል።\n\nማህበረሰቡን ለማሻሻል ስለረዳችን እናመሰግናለን!",
            'complaint_failed': "ቅሬታ ማስገባት አልተቻለም። እባክዎ ቆይተው እንደገና ይሞክሩ።",
            'admin_complaint_notification': "🚨 አዲስ ቅሬታ ተቀብሏል\n\nተጠቃሚ፡ {first_name} (መለያ፡ {user_id})\nየተጠቃሚ ስም፡ {username}\nአይነት፡ {type}\nቅሬታ፡ {text}\n\nሰዓት፡ {time}",
            
            # Language settings
            'language_settings': "🌐 የቋንቋ ቅንብሮች\n\nአሁን ያለው ቋንቋ፡ {current_lang}\n\nየሚፈልጉትን ቋንቋ ይምረጡ፡",
            'language_updated': "✅ ቋንቋዎ ተዘምኗል!\n\nቋንቋዎ ወደ {language} ተቀምጧል።\n\nቦቱ አሁን ለሁሉም ግንኙነቶች ይህን ቋንቋ ይጠቀማል።",
            'language_update_failed': "ቋንቋ ማዘመን አልተቻለም። እባክዎ እንደገና ይሞክሩ።",
            
            # Coin system
            'buy_coins': "💰 ሳንቲሞች ይግዙ",
            'package_selected': "🛒 የተመረጠ ጥቅል፡ {package}\n\n{coins} ሳንቲሞች - ${price}\n\n💰 የክፍያ መመሪያዎች፡\n1. ${price} በሚከተለው መንገድ ይላኩ፡\n   • 💳 ክሬዲት ካርድ\n   • 📱 ሞባይል ክፍያ\n   • 🌐 ኦንላይን ማስተላለፊያ\n\n2. የክፍያ ማረጋገጫ ስክሪንሾት ያንሱ\n3. ስክሪንሾቱን እዚህ ይላኩ\n\nከማረጋገጫ በኋላ፣ ሳንቲሞች በ24 ሰዓታት ውስጥ ወደ መለያዎ ይጨመራሉ።",
            'payment_screenshot_received': "✅ የክፍያ ስክሪንሾት ተቀብሏል!\n\nክፍያዎ በግምገማ ላይ ነው። ከተሰራ በኋላ እንገናኝዎታለን።\n\n⏳ የማስኬድ ጊዜ፡ በተለምዶ በ24 ሰዓታት ውስጥ\n📞 ድጋፍ፡ ጥያቄ ካለዎት @admin ያነጋግሩ",
            'invalid_screenshot': "እባክዎ የክፍያ ማረጋገጫ ስክሪንሾት ይላኩ።\n\nችግር ካጋጠመዎት፣ @admin ያነጋግሩ።",
            'payment_cancelled': "❌ የክፍያ ሂደት ተሰርዟል።",
            
            # Admin commands
            'admin_only': "❌ የአስተዳዳሪ ብቻ ትእዛዝ።",
            'addcoins_usage': "አጠቃቀም፡ /addcoins <የተጠቃሚ_መለያ> <የሳንቲም_ብዛት> [ምክንያት]",
            'user_not_found': "❌ ተጠቃሚ አልተገኘም።",
            'coins_added_success': "✅ ሳንቲሞች በተሳካ ሁኔታ ጨመረ!\n\nተጠቃሚ፡ {first_name} (መለያ፡ {user_id})\nየተጨመሩ ሳንቲሞች፡ {amount}\nአዲስ ሚዛን፡ {balance} ሳንቲሞች\nምክንያት፡ {reason}",
            'coins_added_failed': "❌ ሳንቲሞች ማከል አልተቻለም።",
            'invalid_user_id': "❌ የተጠቃሚ መለያ ወይም የሳንቲም ብዛት ትክክል አይደለም። አጠቃቀም፡ /addcoins <የተጠቃሚ_መለያ> <የሳንቲም_ብዛት> [ምክንያት]",
            'coins_added_user_notification': "🎉 ሳንቲሞች ወደ መለያዎ ጨመረ!\n\n{amount} ሳንቲሞች ወደ መለያዎ ተጨምረዋል።\n\n💰 አዲስ ሚዛን፡ {balance} ሳንቲሞች\n\nምክንያት፡ {reason}",
            'payment_approved_user': "🎉 ክፍያ ተፅዕኖ ተደርጓል!\n\n{amount} ሳንቲሞች ወደ መለያዎ ተጨምረዋል!\n\n💰 አዲስ ሚዛን፡ {balance} ሳንቲሞች\n\nለግዢዎ እናመሰግናለን! 🎊",
            'payment_rejected_user': "❌ ክፍያ ተቀባይነት አላገኘም\n\nክፍያዎ ተቀባይነት አላገኘም። ተጨማሪ መረጃ ለማግኘት @admin ያነጋግሩ።\n\nስህተት ነው ብለው ካሰቡ፣ የግብይት ዝርዝሮችዎን ለድጋፍ ያቅርቡ።",
            'no_pending_payments': "✅ ምንም በጥበቃ ላይ ያሉ ክፍያዎች የሉም።",
            'pending_payments_count': "📋 በጥበቃ ላይ ያሉ ክፍያዎች፡ {count}",
            'payment_info': "የክፍያ መለያ፡ #{id}\nተጠቃሚ፡ {first_name} (መለያ፡ {user_id})\nየተጠቃሚ ስም፡ @{username}\nጥቅል፡ {package}\nመጠን፡ ${price}\nሳንቲሞች፡ {coins}\nሰዓት፡ {time}\n\nሳንቲሞችን በእጅ ለመጨመር /addcoins {user_id} {coins} ይጠቀሙ",
            
            # Account deletion
            'delete_account_warning': "🚨 መለያ ሰርዝ\n\n⚠️ ይህ እርምጃ ዘላቂ ነው እና ሊመለስ አይችልም!\n\nምን ይሰረዛል፡\n• የመገለጫ መረጃዎ\n• ሁሉም ፎቶዎችዎ\n• ማጣጣሚያዎችዎ እና አብዝተኞች\n• መልዕክቶችዎ\n• የመለያ መረጃዎ\n\nመለያዎን ለማስወገድ እርግጠኛ ነዎት?",
            'account_deleted_success': "✅ መለያዎ በተሳካ ሁኔታ ተሰርዟል!\n\nመለያዎ እና ሁሉም የተያያዙ መረጃዎች ዘላቂ ተሰርዘዋል።\n\nለመሄድዎ እናዝናለን! አስተያየት ከቀየሩ፣ ሁልጊዜ አዲስ መለያ በ /start መፍጠር ይችላሉ።\n\nለማህበረሰባችን አባል ስለሆኑ እናመሰግናለን! 👋",
            'account_deleted_failed': "❌ መለያ ማስወገድ አልተቻለም\n\nመለያዎን በማስወገድ ላይ ስህተት ተፈጥሯል። እባክዎ ቆይተው እንደገና ይሞክሩ ወይም ድጋፍ ያነጋግሩ።",
            'account_deletion_cancelled': "✅ የመለያ ማስወገድ ተሰርዟል\n\nመለያዎ አልተሰረዘም።\n\nለመቆየትዎ ደስ ብሎናል! 😊",
            'admin_account_deleted': "🗑️ ተጠቃሚ {user_id} መለያውን ሰርዟል።",
            
            # Utility commands
            'no_operation_cancel': "ለማቆም ንቁ አሠራር የለም።",
            'operation_cancelled': "✅ አሠራሩ ተሰርዟል።",
            'inline_operation_cancelled': "❌ አሠራሩ ተሰርዟል።",
            
            # Help command
            'help_text': """
🤖 ኢትዮጵያ ኮንንት ቦት - የትእዛዝ መመሪያ

🔍 መፈለጊያ እና ማጣጣሚያ፡
• `/browse` - አዳዲስ መገለጫዎችን ይፈልጉ
• `/likes` - መገለጫዎን የወደዱትን ይመልከቱ  
• `/matches` - የጋራ ማጣጣሚያዎችዎን ይመልከቱ

👤 የመገለጫ አስተዳደር፡
• `/profile` - መገለጫዎን ይመልከቱ
• `/language` - የቦቱን ቋንቋ ይቀይሩ

💰 ፕሪሚየም ባህሪያት፡
• `/buycoins` - ለፕሪሚየም ባህሪያት ሳንቲሞች ይግዙ

🛡️ ደህንነት እና ድጋፍ፡
• `/complain` - ችግሮችን ሪፖርት ያድርጉ ወይም አስተያየት ይላኩ
• `/deleteaccount` - መለያዎን ዘላቂ ሰርዙ

💌 መልዕክት መላክ፡
• መገለጫዎችን ሲያሰሩ መልዕክት ለመላክ ኢንላይን ቁልፎችን ይጠቀሙ

🛠 የፕሮግራም ትእዛዞች፡
• `/help` - ይህን የእገዛ መልእክት አሳይ
• `/cancel` - የአሁኑን አሠራር ይቅር

💡 ምክር፡ ለመሰረታዊ ባህሪያት ፈጣን መዳረሻ ለማግኘት የምናሌ ቁልፎችን ይጠቀሙ!
            """,
            
            # Complaint types
            'complaint_type_1': "ተገቢ ያልሆኑ ፎቶዎች",
            'complaint_type_2': "አሰታውቅ ወይም ማጭበርበር", 
            'complaint_type_3': "ሐሰተኛ መገለጫ",
            'complaint_type_4': "ስፓም",
            'complaint_type_5': "ስህተት/ቴክኒካል ችግር",
            'complaint_type_6': "ክፍያ/የደንበኝነት ችግር",
            'complaint_type_7': "የባህሪ ጥያቄ",
            'complaint_type_8': "ሌላ",
            
            # Language names
            'language_english': "🇬🇧 English",
            'language_amharic': "🇪🇹 Amharic",
            'language_oromo': "🇪🇹 Affan Oromo",
            'language_tigrigna': "🇪🇹 Tigrinya",
            'incomplete_profile_registration': "እባክዎ መጀመሪያ ምዝገባዎን በ /start ይጨርሱ",
            'total_photos_count': "{count} ፎቶዎች አሎት።",
            'messages_empty': "📨 መልዕክቶችዎ ሲመጡ እዚህ ይታያሉ።\nሰዎችን ለማገናኘት መገለጫዎችን መሰረም ይጀምሩ!",
            'profile_unknown': "የማይታወቅ",
            'profile_language': "🗣️ {profile_language}  |  🌍 {city}",
            'profile_city_not_specified': "አልተገለጸም",
            'profile_religion_not_specified': "አልተገለጸም",
            'profile_balance': "💰 ሚዛን፡ {coins} ሳንቲም(ዎች)",
            
            # Stats formatting (keep emojis as requested)
            'profile_stats': "❤️ Likes: {likes}   🤝 Matches: {matches}",
            
            # Lists formatting
            'no_likes_yet_list': "እስካሁን ምንም አብዝተኞች የሉም።",
            'likes_list_header': "❤️ መገለጫዎን የወደዱት ተጠቃሚዎች፡\n\n",
            'no_matches_yet_list': "እስካሁን ምንም ማጣጣሚያዎች የሉም።",
            'matches_list_header': "💕 የእርስዎ የጋራ ማጣጣሚያዎች፡\n\n",

            # Errors
            'error': "❌ ስህተት",
            'try_again': "እባክዎ እንደገና ይሞክሩ።",
        },
        
        'oromo': {
            # Registration flow
            'welcome': "👋 Baga nagaan dhuftanii Ethiopia Connect!",
            'choose_language': "Maaloo afaan filadhu:",
            'enter_name': "Gaari! Amma maqaa kee guutuu galchii:",
            'share_contact': "📞 Bilbila kee nu qoodi:",
            'enter_age': "📅 Umuriin kee meeqa?",
            'choose_gender': "👤 Saala kee filadhu:",
            'choose_religion': "🙏 Amantii kee filadhu:",
            'share_location': "📍 Iddoo kee nu qoodi:",
            'choose_city': "🏙️ Magaalaa filadhu:",
            'enter_bio': "📝 Waa'ee keetti nu himi:",
            'share_photos': "📸 Suuraa kee nu ergi (lamatu gahaa):",
            'photo_received': "✅ Suuraa {count} nu ga'e! Dabalataa ergi yookiin /done jedhi",
            'registration_complete': "✅ Galmeen xumurame! 🎉",
            
            # Main menu
            'find_matches': "🔍 Walqabsiisota Barbaadi",
            'my_profile': "👤 Profaayili Koo", 
            'my_messages': "💌 Ergaa Koo",
            
            # Matching
            'no_matches': "😔 Profaayili hin argamu. Eegaa!",
            'all_profiles_seen': "🎉 Profaayilon hunda argite!",
            'nice_profile': "🔥 Profaayili gaari! Muuxannoo gochuu qabdu?",
            'like': "❤️ Jaalala",
            'message': "💌 Ergaa",
            'skip': "⏭️ Darbi",
            
            # Profile commands
            'no_likes': "😔 Hanga ammaatti namni hin jaalalle.",
            'likes_count': "❤️ Namni {count} si jaalale!",
            'no_matches_cmd': "💔 Hanga ammaatti walqabsiisota hin qabdu.",
            'matches_count': "💕 Walqabsiisota {count} qabda!",
            
            # Other features
            'complaint_success': "✅ Daa'imaa kee nu ga'e!",
            'language_updated': "✅ Afaan kee {language} ta'ee jira",
            'screenshot_received': "✅ Kaffaltiin kee nu ga'e! Ilaalamuu jira.",
            'account_deleted': "✅ Akaawuntiin kee delete goffame!",
            'cancel': "❌ Dhiisi",
            'registration_start': "Maaloo afaan filadhu:",
            'name_prompt': "Gaari! Amma maqaa kee guutuu galchii:",
            'invalid_name': "Maaloo maqaa sirrii galchii (yartuuu herrega 2):",
            'contact_prompt': "Maaloo bilbila kee qoodu:",
            'share_contact_button': "📱 Bilbila Qoodi",
            'age_prompt': "Umuriin kee meeqa? (Maaloo umura kee galchii):",
            'invalid_age_range': "Maaloo umuriin sirrii {min_age} irraa {max_age} gidduu galchii:",
            'invalid_age_number': "Maaloo lakkoofsa sirrii umuraaf galchii:",
            'gender_prompt': "Maaloo saala kee filadhu:",
            'religion_prompt': "Maaloo amantii kee filadhu:",
            'location_prompt': "Maaloo iddoo kee qoodi yookiin magaalaa filadhu:",
            'city_choice_prompt': "Maaloo magaalaa filadhu:",
            'bio_prompt': "Maaloo waa'ee keetti nu himi (jaalalloo kee, sochiiwwan kee, fa'i):",
            'photos_prompt': "Yartuuu suuraa lamatu ofii kee irraa ergi:",
            'duplicate_photo': "Suuraan kun dursee ergiteera. Suuraa biraa ergi.",
            'photo_added': "Suuraan profaayili keetti dabalame!",
            'photos_save_error': "Suuraa kee qusachuun hin dandeenye. Irra deebi'i.",
            'registration_success': "Amma walqabsiisota barbaaduu fi namoota waliin dubbachuu dandeessa.",
            'incomplete_registration': "Maaloo dursee galmee kee /start waliin guuti",
            'no_photos_profile': "Maaloo dursee profaayilii kee guutiifi suuraa dabalchi",
            'incomplete_profile': "Maaloo dursee profaayilii kee guuti",
            'fetching_matches': "🔄 Walqabsiisota haaraa siif barbaaduu jira...",
            'no_fresh_matches': "😔 Profaayilii haaraa hin jiru. Eegaa!",
            'profile_setup_required': "❌ Maaloo profaayilii kee guuti",
            'like_sent': "❤️ Jaalala ergame!",
            'already_liked': "Profaayilii kana dursee jaalalateera!",
            'skipped': "⏭️ Darbi",
            'user_not_found': "Fayyadamaa hin argamne",
            'write_message_to': "💌 {first_name} f ergaa barreessi:",
            'error_try_again': "Dogoggora: Maaloo irra deebi'i",
            'message_sent': "✅ Ergaa ergame!",
            'message_delivery_failed': "❌ Ergaa hin ga'ne. Fayyadamaan bot dhiisee jiraachuu danda'a.",
            'message_send_error': "❌ Ergaa erguu keessatti dogoggora. Maaloo irra deebi'i.",
            'write_reply_to': "💌 {first_name} f deebii barreessi:",
            'profile_not_found': "Profaayilii hin argamne",
            'total_photos': "Suuraa {count} qabda.",
            'profile_error': "Profaayilii agarsiisuu hin dandeenye",
            'user_blocked': "🚫 Fayyadamaa cufame",
            'block_success': "Fayyadamaa cufame. Profaayilii isaa eega ammaa argachuu hin dandeessu.",
            'block_error': "❌ Fayyadamaa cufuu keessatti dogoggora",
            'cancelled': "❌ Dhiifame",
            
            # Profile display texts
            'profile_display_error': "Profaayilii agarsiisuu hin dandeenye. Maaloo irra deebi'i.",
            'unknown_user': "Fayyadamaa",
            
            # Additional matching texts
            'all_profiles_seen': "🎉 Profaayilon hunda argite!\nWalqabsiisota haaraa eegaa!",
            'no_matches_found': "😔 Yeroo ammaa kana profaayilii haaraa hin argamu.\nEegaa!",
            'action_prompt': "🔥 Profaayilii gaari! Muuxannoo gochuu qabdu?",
            'no_likes_yet': "Hanga ammaatti namni hin jaalalle.\nItti fufiinsa argachuuf itti fufi!",
    'likes_count': "Namni {count} profaayilii kee jaalale!\n\nIsaan deebisuuf /browse fayyadami!",
    'liker_number': "Jaalallee #{number}",
    'someone_liked_back': "🔥 Namni si jaalale{extra_photos}! Jaallatteettaa?",
    'no_matches_yet': "Hanga ammaatti walqabsiisota hin qabdu.\nWalqabsiisota argachuuf /browse fayyadami!",
    'matches_count': "💕 Walqabsiisota {count} qabda!\n\nKun walqabsiisota keeti:",
    'match_number': "Walqabsiisaa #{number}",
    'its_a_match': "💕 Walqabsiisa{extra_photos}! Haasa'a eegaluu qabdu?",
    
    # Complaint system
    'complain_prompt': "📝 Daa'imaa Galchi\n\nLakkoofsa ergee sababa filadhu:\n\n1. Suuraa hin faankessine\n2. Rukuttaa yookiin bullaa'umsa\n3. Profaayilii sobaa\n4. Spam\n5. Dogoggora/Teknikaalaa\n6. Kaffaltii/Hojii dhuunfaa\n7. Filannoo meeshaa\n8. Kan biraa\n\nLakkoofsa (1-8) galchii:\nYookiin /cancel jedhi ittisuu",
    'complaint_type_selected': "📝 Gosa Daa'imaa: {type}\n\nDaa'imaa kee guutuu nuuf himi (dachaa 500 qopheessitoota):\n\nDaa'imaa kee gadi galchii:\nYookiin /cancel jedhi ittisuu",
    'invalid_complaint_number': "Lakkoofsa sirrii 1-8 gidduu galchii:",
    'complaint_cancelled': "✅ Daa'imaa dhiifame.",
    'complaint_too_short': "Dabalataan nuuf himi (yartuuu qopheessitoota 10).",
    'complaint_too_long': "Daa'imaan kun dheeraa hedduu dha. Qopheessitoota 500 qofatu hayyama.",
    'complaint_submitted': "✅ Daa'imaa Sirriitti Galmaa'e!\n\nNuuf yaada kennitaniif galatoomaa. Gareen keenya daa'imaa kee ilaala, hojii sirrii hojjata.\n\nGaree nuu gargaartanii galatoomaa!",
    'complaint_failed': "Daa'imaa galchuu hin dandeenye. Eegaa irra deebi'i.",
    'admin_complaint_notification': "🚨 Daa'imaa Haaraa Galmaa'e\n\nFayyadamaa: {first_name} (ID: {user_id})\nMaqaa Fayyadamaa: {username}\nGosa: {type}\nDaa'imaa: {text}\n\nYeroo: {time}",
    
    # Language settings
    'language_settings': "🌐 Saagiinsa Afaanii\n\nAmmaa afaan: {current_lang}\n\nAfaan filadhu:",
    'language_updated': "✅ Afaan Sirriitti Jijjirame!\n\nAfaan kee {language} ta'ee jira.\n\nBoti kun amma afaan kana hojii hundaaf fayyadama.",
    'language_update_failed': "Afaan jijjiiruu hin dandeenye. Irra deebi'i.",
    
    # Coin system
    'buy_coins': "💰 Santiimaa Bitadhu",
    'package_selected': "🛒 Paakeejii Filatame: {package}\n\n{coins} Santiimaa - ${price}\n\n💰 Qajeelfama Kaffaltii:\n1. ${price} kana fayyadamuun ergi:\n   • 💳 Kaardii liqii\n   • 📱 Kaffaltii Bilbila\n   • 🌐 Dhaabbata Interneetii\n\n2. Mirkaneessaa kaffaltii screenshot godhadhu\n3. Screenshot achitti nu ergi\n\nMirkaneessaa booda, santiimoon akkaataa sa'aatii 24 keessatti meeshaa keetti dabaltama.",
    'payment_screenshot_received': "✅ Screenshot Kaffaltii Nu Ga'e!\n\nKaffaltiin kee ilaalamuu jira. Yeroo hojjatamu si beeksifna.\n\n⏳ Yeroo Hojii: Yeroo baay'ee sa'aatii 24 keessatti\n📞 Gargaarsa: Yoo gaaffi qabaatte @admin waliin dubbadhu",
    'invalid_screenshot': "Mirkaneessaa kaffaltii screenshot nu ergi.\n\nYoo rakkoo qabaatte, @admin waliin dubbadhu.",
    'payment_cancelled': "❌ Kaffaltii dhiifame.",
    
    # Admin commands
    'admin_only': "❌ Ajaja manahimaa qofa.",
    'addcoins_usage': "Fayyadamuu: /addcoins <ID fayyadamaa> <lakkoofsa santiimaa> [sababa]",
    'user_not_found': "❌ Fayyadamaa hin argamne.",
    'coins_added_success': "✅ Santiimaa Sirriitti Dabalame!\n\nFayyadamaa: {first_name} (ID: {user_id})\nSantiimaa Dabalame: {amount}\nHaala Haaraa: {balance} santiimaa\nSababa: {reason}",
    'coins_added_failed': "❌ Santiimaa dabalchuun hin dandeenye.",
    'invalid_user_id': "❌ ID fayyadamaa ykn lakkoofsa santiimaa dogoggora. Fayyadamuu: /addcoins <ID fayyadamaa> <lakkoofsa santiimaa> [sababa]",
    'coins_added_user_notification': "🎉 Santiimaa Meeshaa Keetti Dabalame!\n\nSantiimaa {amount} meeshaa keetti dabalame.\n\n💰 Haala Haaraa: {balance} santiimaa\n\nSababa: {reason}",
    'payment_approved_user': "🎉 Kaffaltii Hayyame!\n\nSantiimaa {amount} meeshaa keetti dabalame!\n\n💰 Haala Haaraa: {balance} santiimaa\n\nBitaa keetiif galatoomaa! 🎊",
    'payment_rejected_user': "❌ Kaffaltii Dhiifame\n\nKaffaltiin kee dhiifame. Dabalataan @admin waliin dubbadhu.\n\nYoo dogoggora ta'ee jettee amante, oduu transaction kee gargaarsaaf kenni.",
    'no_pending_payments': "✅ Kaffaltii eegamaa hin jiru.",
    'pending_payments_count': "📋 Kaffaltii Eegamaa: {count}",
    'payment_info': "ID Kaffaltii: #{id}\nFayyadamaa: {first_name} (ID: {user_id})\nMaqaa Fayyadamaa: @{username}\nPaakeejii: {package}\nBaay'ina: ${price}\nSantiimaa: {coins}\nYeroo: {time}\n\nSantiimaa harkaan dabalchuu /addcoins {user_id} {coins} fayyadami",
    
    # Account deletion
    'delete_account_warning': "🚨 Akaawuntii Delete Godhi\n\n⚠️ Gocha kana deebisuun hin danda'amu!\n\nMaal delete gooftu:\n• Odeeffannoo profaayilii kee\n• Suuraa kee hunda\n• Walqabsiisota kee fi jaalalloo\n• Ergaa kee\n• Odeeffannoo akaawuntii kee\n\nAkaawuntii kee delete gochuu mirkaneeffatta?",
    'account_deleted_success': "✅ Akaawuntii Sirriitti Delete Goffame!\n\nAkaawuntii kee fi odeeffannoo hunda deletes goffame.\n\nBa'anii keetiif gaddi dha! Yoo maliifte, yeroo hunda akaawuntii haaraa /start waliin uumu dandeessa.\n\nGaree nuu ta'anii galatoomaa! 👋",
    'account_deleted_failed': "❌ Akaawuntii Delete Godhuu Hin Dandeenye\n\nAkaawuntii kee delete godhuu keessatti dogoggora ta'e. Eegaa irra deebi'i yookiin gargaarsa barbaadi.",
    'account_deletion_cancelled': "✅ Akaawuntii Delete Godhuu Dhiifame\n\nAkaawuntii kee hin delete goffamne.\n\nTurtuu keetiif gammadi! 😊",
    'admin_account_deleted': "🗑️ Fayyadamaa {user_id} akaawuntii isaa delete goote.",
    
    # Utility commands
    'no_operation_cancel': "Hojii dhiisuuf hojii hin jiru.",
    'operation_cancelled': "✅ Hojii dhiifame.",
    'inline_operation_cancelled': "❌ Hojii dhiifame.",
    
    # Help command
    'help_text': """
🤖 Botii Ethiopia Connect - Qajeelfama Ajajaa

🔍 Barbaachisaa fi Walqabsiisaa:
• `/browse` - Profaayilii haaraa barbaadi
• `/likes` - Profaayilii kee jaalallee ilaali  
• `/matches` - Walqabsiisota kee ilaali

👤 Bulchiinsa Profaayilii:
• `/profile` - Profaayilii kee ilaali
• `/language` - Afaan botii jijjiiri

💰 Meeshaa Premium:
• `/buycoins` - Meeshaa premium'f santiimaa bitadhu

🛡️ Nageenyaa fi Gargaarsa:
• `/complain` - Rakkoo report godhi yookiin yaada ergi
• `/deleteaccount` - Akaawuntii kee delete godhi

💌 Ergaa Erguu:
• Yeroo profaayilii dubbattu fayyadamaa waliin dubbachuuf button fayyadami

🛠 Ajaja Fayyadamuu:
• `/help` - Qajeelfama kana agarsiisi
• `/cancel` - Hojii ammaa dhiisi

💡 Gorsa: Meeshaa ijoo argachuuf button fayyadami!
    """,
    
    # Complaint types
    'complaint_type_1': "Suuraa Hin Faankessine",
    'complaint_type_2': "Rukuttaa yookiin Bullaa'umsa", 
    'complaint_type_3': "Profaayilii Sobaa",
    'complaint_type_4': "Spam",
    'complaint_type_5': "Dogoggora/Teknikaalaa",
    'complaint_type_6': "Kaffaltii/Hojii Dhuunfaa",
    'complaint_type_7': "Filannoo Meeshaa",
    'complaint_type_8': "Kan Biraa",
    
    # Language names
    'language_english': "🇬🇧 English",
    'language_amharic': "🇪🇹 Amharic",
    'language_oromo': "🇪🇹 Affan Oromo",
    'language_tigrigna': "🇪🇹 Tigrinya",
    'incomplete_profile_registration': "Maaloo dursee galmee kee /start waliin guuti",
            'total_photos_count': "Suuraa {count} qabda.",
            'messages_empty': "📨 Ergaan kee yeroo nu ga'u achitti agarsiifama.\nNamoota waliin dubbachuuf profaayilii dubbisuu eegalu!",
            'profile_unknown': "Kan hin beekamne",
            'profile_language': "🗣️ {profile_language}  |  🌍 {city}",
            'profile_city_not_specified': "Kan hin murtaane",
            'profile_religion_not_specified': "Kan hin murtaane",
            'profile_balance': "💰 Haala: {coins} santiimaa",
            
            # Stats formatting (keep emojis as requested)
            'profile_stats': "❤️ Likes: {likes}   🤝 Matches: {matches}",
            
            # Lists formatting
            'no_likes_yet_list': "Hanga ammaatti jaalalloo hin jiru.",
            'likes_list_header': "❤️ Fayyadamoonni profaayilii kee jaalalan:\n\n",
            'no_matches_yet_list': "Hanga ammaatti walqabsiisota hin jiru.",
            'matches_list_header': "💕 Walqabsiisota kee:\n\n",

            # Errors
            'error': "❌ Dogoggora",
            'try_again': "Maaloo irra deebi'i.",
        },
        
        'tigrigna': {
            # Registration flow
            'welcome': "👋 እንቋዕ ብደሓን መጻእኩም ናብ ኢትዮጵያ ኮንንት!",
            'choose_language': "በጃኹም ቋንቋ ምረጹ:",
            'enter_name': "ጽቡቕ! ሕጂ ምሉእ ስምኩም ኣእትዉ:",
            'share_contact': "📞 ቁጽሪ ስልኪ ክፋል ግበሩ:",
            'enter_age': "📅 ዕድሚኹም ክንደይ እዩ?",
            'choose_gender': "👤 ጾታኩም ምረጹ:",
            'choose_religion': "🙏 ሃይማኖትኩም ምረጹ:",
            'share_location': "📍 ከተማኩም ክፋል ግበሩ:",
            'choose_city': "🏙️ ከተማ ምረጹ:",
            'enter_bio': "📝 ብዛዕባ ገዛእ ርእስኹም ነገሩና:",
            'share_photos': "📸 ስእላትኩም ለኣኹም (ውዲት 2 ይፍቀድ):",
            'photo_received': "✅ ስእል {count} ተቐቢሉ! ተወሳኺ ለኣኹም ወይ /done በሉ",
            'registration_complete': "✅ ምዝገባ ተወዲኡ! 🎉",
            
            # Main menu
            'find_matches': "🔍 ምስማር ደፊር",
            'my_profile': "👤 ፕሮፋይለይ", 
            'my_messages': "💌 መልእኽተይ",
            
            # Matching
            'no_matches': "😔 ፕሮፋይል ኣይተረኽበን። ተጸበዩ!",
            'all_profiles_seen': "🎉 ኩሎም ፕሮፋይላት ረኺብኩም!",
            'nice_profile': "🔥 ጽቡቕ ፕሮፋይል! ክትሰርሑ ድሉዉ ኢኹም?",
            'like': "❤️ ፍቕሪ",
            'message': "💌 መልእኽቲ",
            'skip': "⏭️ ኣልግ",
            
            # Profile commands
            'no_likes': "😔 ክሳዕ ሕጂ ሰብ ኣይፈትወኩምን።",
            'likes_count': "❤️ {count} ሰባት ፈቲዖምካ!",
            'no_matches_cmd': "💔 ክሳዕ ሕጂ ምስማር የለን።",
            'matches_count': "💕 {count} ምስማር ኣለኩም!",
            
            # Other features
            'complaint_success': "✅ ቅሬታኹም ቀሪቡ!",
            'language_updated': "✅ ቋንቋኹም ናብ {language} ተቐይሩ",
            'screenshot_received': "✅ ክፍሊትኩም ተቐቢሉ! ኣብ መጣኒፅ እዩ።",
            'account_deleted': "✅ ኣካውንትኩም ተሰሪዙ!",
            'cancel': "❌ ኣትርፍ",
            'registration_start': "በጃኹም ቋንቋ ምረጹ:",
            'name_prompt': "ጽቡቕ! ሕጂ ምሉእ ስምኩም ኣእትዉ:",
            'invalid_name': "በጃኹም ልክዕ ስም ኣእትዉ (ውዱብ 2 ፊደላት):",
            'contact_prompt': "በጃኹም ቁጽሪ ስልኪ ክፋል ግበሩ:",
            'share_contact_button': "📱 ቁጽሪ ስልኪ ክፋል ግበሩ",
            'age_prompt': "ዕድሚኹም ክንደይ እዩ? (በጃኹም ዕድሚኹም ኣእትዉ):",
            'invalid_age_range': "በጃኹም ልክዕ ዕድሜ ካብ {min_age} ክሳዕ {max_age} ኣእትዉ:",
            'invalid_age_number': "በጃኹም ንዕድሜኹም ልክዕ ቁጽሪ ኣእትዉ:",
            'gender_prompt': "በጃኹም ጾታኩም ምረጹ:",
            'religion_prompt': "በጃኹም ሃይማኖትኩም ምረጹ:",
            'location_prompt': "በጃኹም ከተማኩም ክፋል ግበሩ ወይ ከተማ ምረጹ:",
            'city_choice_prompt': "በጃኹም ካብ ኣብ ታሕቲ ዘሎ ዝርዝር ከተማ ምረጹ:",
            'bio_prompt': "በጃኹም ብዛዕባ ገዛእ ርእስኹም ነገሩና (ፍቕርኩም፣ ንጥፈታትኩም፣ ወዘተ.):",
            'photos_prompt': "በጃኹም ውዲት 2 ግልጽ ዝዀኑ ስእላት ለኣኹም",
            'duplicate_photo': "እዚ ስእሊ ኣቐዲምኩም ለኢኹምዎ። በጃኹም ካልእ ስእሊ ለኣኹም።",
            'photo_added': "ስእሊ ናብ ፕሮፋይልኩም ተወሲኑ!",
            'photos_save_error': "ስእላትኩም ምዕቃብ ኣይተኻእለን። በጃኹም ደጊምኩም ፈትኑ።",
            'registration_success': "ሕጂ ምስማር ክትረኽቡ ከምኡ'ውን ሰባት ክትበሉ ትኽእሉ ኢኹም።",
            'incomplete_registration': "በጃኹም ቀዳምነት ምዝገባኹም ብ /start ኣጅምሩ",
            'no_photos_profile': "በጃኹም ቀዳምነት ፕሮፋይልኹም ኣጅምሩ ከምኡ'ውን ስእላት ኣእትዉ",
            'incomplete_profile': "በጃኹም ቀዳምነት ፕሮፋይልኹም ኣጅምሩ",
            'fetching_matches': "🔄 ሓድሽ ምስማር ንኹም ኣብ ምድላይ...",
            'no_fresh_matches': "😔 ክሳዕ ሕጂ ሓድሽ ፕሮፋይላት የለን። ተጸበዩ!",
            'profile_setup_required': "❌ በጃኹም ፕሮፋይልኹም ኣጅምሩ",
            'like_sent': "❤️ ፍቕሪ ተልኢኹዎ!",
            'already_liked': "እዚ ፕሮፋይል ኣቐዲምኩም ፈቲዖምዎ!",
            'skipped': "⏭️ ኣልግ",
            'user_not_found': "ተጠቃሚ ኣይተረኽበን",
            'write_message_to': "💌 ን {first_name} መልእኽቲ ጽሓፉ:",
            'error_try_again': "ጌጋ፡ በጃኹም ደጊምኩም ፈትኑ",
            'message_sent': "✅ መልእኽቲ ተልኢኹዎ!",
            'message_delivery_failed': "❌ መልእኽቲ ክዕለን ኣይከኣለን። ተጠቃሚ እቲ ቦት ከም ዘጋጠመ ይኩን።",
            'message_send_error': "❌ መልእኽቲ ምልኣኽ ኣጋጢሙ። በጃኹም ደጊምኩም ፈትኑ።",
            'write_reply_to': "💌 ን {first_name} መልሲ ጽሓፉ:",
            'profile_not_found': "ፕሮፋይል ኣይተረኽበን",
            'total_photos': "{count} ስእላት ኣለዎም።",
            'profile_error': "ፕሮፋይል ምርኢት ኣጋጢሙ",
            'user_blocked': "🚫 ተጠቃሚ ተኣጊዱ",
            'block_success': "ተጠቃሚ ተኣጊዱ። ፕሮፋይሉ ካብ ሕጂ ንደሓር ኣይትርኢን ኢኻ።",
            'block_error': "❌ ተጠቃሚ ምእጋድ ኣጋጢሙ",
            'cancelled': "❌ ተሰሪዙ",
            
            # Profile display texts
            'profile_display_error': "ፕሮፋይል ምርኢት ኣጋጢሙ። በጃኹም ደጊምኩም ፈትኑ።",
            'unknown_user': "ተጠቃሚ",
            
            # Additional matching texts
            'all_profiles_seen': "🎉 ኩሎም እተርከቡ ፕሮፋይላት ረኺብኩም!\nሓድሽ ምስማር ንምርኣይ ተጸበዩ!",
            'no_matches_found': "😔 ኣብ እዋን እዚ ሓድሽ ፕሮፋይላት ኣይተረኽቡን።\nተጸበዩ!",
            'action_prompt': "🔥 ጽቡቕ ፕሮፋይል! ክትሰርሑ ድሉዉ ኢኹም?",
            'no_likes_yet': "ክሳዕ ሕጂ ሰብ ኣይፈትወኩምን።\nተጸበዩ ንዝያዳ ርእይቶ ክትረኽቡ!",
    'likes_count': "{count} ሰባት ፕሮፋይልኩም ፈቲዖምዎ!\n\nንሳቶም ክፈትዉ ከምኡ'ውን ምስማር ንምፍጣር /browse ተጠቐሙ!",
    'liker_number': "ፈታዊ #{number}",
    'someone_liked_back': "🔥 ሓደ ሰብ ፈቲዑኻ{extra_photos}! ኣገዳሲ ዲኻ?",
    'no_matches_yet': "ክሳዕ ሕጂ ምንም ምስማር የለን።\nምስማር ንምርካብ ፕሮፋይላት ብ /browse ክትፈትዉ ጀምሩ!",
    'matches_count': "💕 {count} ምስማር ኣለኩም!\n\n�ንዞም ዝተኻፈሉ ምስማርኩም እዮም፡",
    'match_number': "ምስማር #{number}",
    'its_a_match': "💕 ምስማር እዩ{extra_photos}! ዘመድ ክትጅምሩ ትደልዩ?",
    
    # Complaint system
    'complain_prompt': "📝 ቅሬታ ኣስግድ\n\nቁጽሩ ብምልኣኽ ምኽንያት ምረጹ፡\n\n1. ዘይግቡእ ስእላት\n2. ምዕባለ ወይ ምጭባጥ\n3. ሓሰተኛ ፕሮፋይል\n4. ስፓም\n5. ጌጋ/ቴክኒካላዊ ጸገም\n6. ክፍሊት/ደንበኝነት ጸገም\n7. ባህርያት ሕቶ\n8. ካልእ\n\nቁጽሩ ኣእትዉ (1-8)፡\nወይ /cancel ኣእትዉ ንምቁራጽ",
    'complaint_type_selected': "📝 ዓይነት ቅሬታ፡ {type}\n\nበጃኹም ቅሬታኹም ብዝሕግዝ ግለጹ (ከቢድ 500 ፊደላት)፡\n\nቅሬታኹም ኣብ ታሕቲ ኣእትዉ፡\nወይ /cancel ኣእትዉ ንምቁራጽ",
    'invalid_complaint_number': "በጃኹም ቅኑዕ ቁጽሪ ካብ 1-8 ኣእትዉ፡",
    'complaint_cancelled': "✅ ቅሬታ ተሰሪዙ።",
    'complaint_too_short': "በጃኹም ዝያዳ ዝርዝር ኣቕርቡ (ውዱብ 10 ፊደላት)።",
    'complaint_too_long': "ቅሬታ ኣዝዩ ነዊሕ እዩ። ከቢድ 500 ፊደላት ጥራይ እዩ ዚፍቀድ።",
    'complaint_submitted': "✅ ቅሬታ ብትኽክል ቀሪቡ!\n\n�ንርእይቶኹም ኣመስግና ኢና። ጋንኑና ቅሬታኹም ኪመርጽ ከምኡ'ውን ኣግባብ ዘለዎ እምቢታ ኪወስድ እዩ።\n\nማሕበረሰብ ንምህዋጽ ስለ ዝሓገዙና ኣመስግና ኢና!",
    'complaint_failed': "ቅሬታ ምስጋን ኣይተኻእለን። በጃኹም ደጊምኩም ፈትኑ።",
    'admin_complaint_notification': "🚨 ሓድሽ ቅሬታ ቀሪቡ!\n\nተጠቃሚ፡ {first_name} (መለይ፡ {user_id})\nተጠቃሚ ስም፡ {username}\nዓይነት፡ {type}\nቅሬታ፡ {text}\n\nሰዓት፡ {time}",
    
    # Language settings
    'language_settings': "🌐 ቋንቋ ቅጥዒ\n\nኣሁኑ ቋንቋ፡ {current_lang}\n\n�ቲ ዚፈቱዎ ቋንቋ ምረጹ፡",
    'language_updated': "✅ ቋንቋኹም ብትኽክል ተቐይሩ!\n\n�ቋንቋኹም ናብ {language} ተቐሚጡ።\n\n�ቦት ካብ ሕጂ ንኹሉ ርክባት ነዚ ቋንቋ እዩ ዚጥቀመሉ።",
    'language_update_failed': "ቋንቋ ምቕያር ኣይተኻእለን። በጃኹም ደጊምኩም ፈትኑ።",
    
    # Coin system
    'buy_coins': "💰 ሳንቲም ይግዙ",
    'package_selected': "🛒 ዝተመረጠ ጥቅል፡ {package}\n\n{coins} ሳንቲም - ${price}\n\n💰 መመርዒ ክፍሊት፡\n1. ${price} በዚ መንገድ ኣልዙ፡\n   • 💳 ክሬዲት ካርድ\n   • 📱 ሞባይል ክፍሊት\n   • 🌐 ኦንላይን ምልዋይ\n\n2. ናይ ክፍሊት ኣረጋግጽ ስክሪንሾት ይውሰዱ\n3. ስክሪንሾት ኣብዚ ኣልዙ\n\nድሕሪ ምርግጋጽ፡ ሳንቲም ኣብ 24 ሰዓታት ናብ ኣካውንትኹም ኪወሃብ እዩ።",
    'payment_screenshot_received': "✅ ናይ ክፍሊት ስክሪንሾት ተቐቢሉ!\n\nክፍሊትኹም ኣብ ትሕዝቶ እዩ። ክጸንሐ ከሎ ንነግርኩም።\n\n⏳ ግዜ ምጽዓን፡ ብመብዛሕትኡ 24 ሰዓታት\n📞 ሓገዝ፡ ሕቶ እንተለኩም @admin ተራኸቡ",
    'invalid_screenshot': "በጃኹም ናይ ክፍሊት ኣረጋግጽ ስክሪንሾት ኣልዙ።\n\nጸገም እንተለኩም፡ @admin ተራኸቡ።",
    'payment_cancelled': "❌ ናይ ክፍሊት ሂደት ተሰሪዙ።",
    
    # Admin commands
    'admin_only': "❌ ናይ ኣስተዳደሪ ትእዛዝ ጥራይ።",
    'addcoins_usage': "ኣጠቓቕማ፡ /addcoins <ተጠቃሚ መለይ> <ብዝሒ ሳንቲም> [ምኽንያት]",
    'user_not_found': "❌ ተጠቃሚ ኣይተረኽበን።",
    'coins_added_success': "✅ ሳንቲም ብትኽክል ተወሲኑ!\n\nተጠቃሚ፡ {first_name} (መለይ፡ {user_id})\nሳንቲም ተወሲኑ፡ {amount}\nሓድሽ ሚዛን፡ {balance} ሳንቲም\nምኽንያት፡ {reason}",
    'coins_added_failed': "❌ ሳንቲም ምውሳን ኣይተኻእለን።",
    'invalid_user_id': "❌ ዘይቅኑዕ ተጠቃሚ መለይ ወይ ብዝሒ ሳንቲም። ኣጠቓቕማ፡ /addcoins <ተጠቃሚ መለይ> <ብዝሒ ሳንቲም> [ምኽንያት]",
    'coins_added_user_notification': "🎉 ሳንቲም ናብ ኣካውንትኹም ተወሲኑ!\n\nሳንቲም {amount} ናብ ኣካውንትኹም ተወሲኑ።\n\n💰 ሓድሽ ሚዛን፡ {balance} ሳንቲም\n\nምኽንያት፡ {reason}",
    'payment_approved_user': "🎉 ክፍሊት ተፅዕኖ ተዋሂቡ!\n\nሳንቲም {amount} ናብ ኣካውንትኹም ተወሲኑ!\n\n💰 ሓድሽ ሚዛን፡ {balance} ሳንቲም\n\n�ንግዝኻ ኣመስግና ኢና! 🎊",
    'payment_rejected_user': "❌ ክፍሊት ኣይተቐበለን\n\nክፍሊትኩም ኣይተቐበለን። ዝያዳ ሓበሬታ ንምርካብ @admin ተራኸቡ።\n\nጌጋ ኮይኑ እንተሓሰብኩም፡ ዝኸውን ሓበሬታ ናብ ሓገዝ ኣቕርቡ።",
    'no_pending_payments': "✅ ዝጸበቡ ክፍልታት የለን።",
    'pending_payments_count': "📋 ዝጸበቡ ክፍልታት፡ {count}",
    'payment_info': "መለይ ክፍሊት፡ #{id}\nተጠቃሚ፡ {first_name} (መለይ፡ {user_id})\nተጠቃሚ ስም፡ @{username}\nጥቅል፡ {package}\nብዝሒ፡ ${price}\nሳንቲም፡ {coins}\nሰዓት፡ {time}\n\nሳንቲም ብኢድ ንምውሳን /addcoins {user_id} {coins} ተጠቐሙ",
    
    # Account deletion
    'delete_account_warning': "🚨 ኣካውንት ሰርዝ\n\n⚠️ እዚ ተግባር እዚ ዘይምለስ እዩ!\n\nእንታይ ኪስረዝ፡\n• ፕሮፋይል ሓበሬታኹም\n• ኩሉ ስእልኹም\n• ምስማርኹም ከምኡ'ውን ፍቕሪኹም\n• መልእኽትኹም\n• ኣካውንት ሓበሬታኹም\n\nኣካውንትኹም ንምስረዝ ርግጸኛ ኢኹም?",
    'account_deleted_success': "✅ ኣካውንት ብትኽክል ተሰሪዙ!\n\nኣካውንትኹም ከምኡ'ውን ኩሉ ተዛመድቲ ሓበሬታ ተሰሪዙ።\n\nምእንቲ ምኻድኩም ይሕዛና! ሓሳብ እንተቀየርኩም፡ ኩሉ ግዜ ሓድሽ ኣካውንት ብ /start ክትፈጥሩ ትኽእሉ።\n\nኣባል ማሕበረሰብና ስለ ዝኾንኩም ኣመስግና ኢና! 👋",
    'account_deleted_failed': "❌ ኣካውንት ምስረዝ ኣይተኻእለን\n\nኣካውንትኹም ኣብ ምስረዝ ጌጋ ኣጋጢሙ። በጃኹም ደጊምኩም ፈትኑ ወይ ሓገዝ ተራኸቡ።",
    'account_deletion_cancelled': "✅ ናይ ኣካውንት ምስረዝ ተሰሪዙ\n\nኣካውንትኹም ኣይተሰረዘን።\n\nምእንቲ ምጽናሕኩም ሕጉስ ኢና! 😊",
    'admin_account_deleted': "🗑️ ተጠቃሚ {user_id} ኣካውንቱ ሰሪዙ።",
    
    # Utility commands
    'no_operation_cancel': "ንምቁራጽ ንቑ ናይ ስራሕ የለን።",
    'operation_cancelled': "✅ ናይ ስራሕ ተሰሪዙ።",
    'inline_operation_cancelled': "❌ ናይ ስራሕ ተሰሪዙ።",
    
    # Help command
    'help_text': """
🤖 ኢትዮጵያ ኮንንት ቦት - መምርሒ ትእዛዝ

🔍 ምድላይ ከምኡ'ውን ምስማር፡
• `/browse` - ሓድሽ ፕሮፋይላት ድለዩ
• `/likes` - ፕሮፋይልኩም ዝፈትዉ ሰባት ርአዩ  
• `/matches` - ዝተካፈለ ምስማርኩም ርአዩ

👤 ምምሕዳር ፕሮፋይል፡
• `/profile` - ፕሮፋይልኩም ርአዩ
• `/language` - ቋንቋ ቦት ቀይሩ

💰 ፕሪሚየም ባህርያት፡
• `/buycoins` - ንፕሪሚየም ባህርያት ሳንቲም ይግዙ

🛡️ ጸጥታ ከምኡ'ውን ሓገዝ፡
• `/complain` - ጸገማት ሪፖርት ግበሩ ወይ ርእይቶ ኣልዩ
• `/deleteaccount` - ኣካውንትኩም ሰርዩ

💌 መልእኽቲ ምልኣኽ፡
• ፕሮፋይላት ምስ ዝድለዩ መልእኽቲ ንምልኣኽ ኢንላይን ቁልፍ ተጠቐሙ

🛠 ናይ ስራሕ ትእዛዝ፡
• `/help` - እዚ መምርሒ መልእኽቲ ኣርእዩ
• `/cancel` - ናይ ሕጂ ስራሕ ቁረጹ

💡 ምኽር፡ ንመበገሲ ባህርያት ቅልጡፍ መድረሽ ንምርካብ ናይ ምናሌ ቁልፍ ተጠቐሙ!
    """,
    
    # Complaint types
    'complaint_type_1': "ዘይግቡእ ስእላት",
    'complaint_type_2': "ምዕባለ ወይ ምጭባጥ", 
    'complaint_type_3': "ሓሰተኛ ፕሮፋይል",
    'complaint_type_4': "ስፓም",
    'complaint_type_5': "ጌጋ/ቴክኒካላዊ ጸገም",
    'complaint_type_6': "ክፍሊት/ደንበኝነት ጸገም",
    'complaint_type_7': "ባህርያት ሕቶ",
    'complaint_type_8': "ካልእ",
    
    # Language names
    'language_english': "🇬🇧 English",
    'language_amharic': "🇪🇹 Amharic",
    'language_oromo': "🇪🇹 Affan Oromo",
    'language_tigrigna': "🇪🇹 Tigrinya",
    'incomplete_profile_registration': "በጃኹም ቀዳምነት ምዝገባኹም ብ /start ኣጅምሩ",
            'total_photos_count': "{count} ስእላት ኣለዎም።",
            'messages_empty': "📨 መልእኽትኹም ምስ ዚመጹ ኣብዚ ኪርአዩ እዮም።\nምስ ሰባት ንምትእስሳር ፕሮፋይላት ክትድለዩ ጀምሩ!",
            'profile_unknown': "ዘይፍለጥ",
            'profile_language': "🗣️ {profile_language}  |  🌍 {city}",
            'profile_city_not_specified': "ዘይተገልጸ",
            'profile_religion_not_specified': "ዘይተገልጸ",
            'profile_balance': "💰 ሚዛን፡ {coins} ሳንቲም",
            
            # Stats formatting (keep emojis as requested)
            'profile_stats': "❤️ Likes: {likes}   🤝 Matches: {matches}",
            
            # Lists formatting
            'no_likes_yet_list': "ክሳዕ ሕጂ ምንም ፈታውቲ የለን።",
            'likes_list_header': "❤️ ፕሮፋይልኩም ዝፈትዉ ተጠቃሚታት፡\n\n",
            'no_matches_yet_list': "ክሳዕ ሕጂ ምንም ምስማር የለን።",
            'matches_list_header': "💕 ዝተካፈሉ ምስማርኩም፡\n\n",
            
            # Errors
            'error': "❌ ጌጋ",
            'try_again': "በጃኹም ደጊምኩም ፈትኑ።",
        }
    }
    
    # Get translation for the key, fallback to English if not found
    lang_translations = translations.get(language, translations['english'])
    text = lang_translations.get(key, translations['english'].get(key, key))
    
    # Format with any provided kwargs
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text