import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import config

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    print("🚀 Starting bot in DEBUG mode...")
    
    # Check if token is loaded
    if not config.BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found in environment variables!")
        print("Please check your .env file")
        return
    
    print(f"✅ Bot token loaded: {config.BOT_TOKEN[:10]}...")
    
    try:
        bot = Bot(token=config.BOT_TOKEN)
        dp = Dispatcher()
        
        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Bot connected successfully: @{me.username} (ID: {me.id})")
        
        # Import and test routers
        print("🔄 Loading routers...")
        
        from handlers.start import router as start_router
        from handlers.profile import router as profile_router
        from handlers.matching import router as matching_router
        
        dp.include_router(start_router)
        dp.include_router(profile_router)
        dp.include_router(matching_router)
        
        # Try to import commands router
        try:
            from handlers.commands import router as commands_router
            dp.include_router(commands_router)
            print("✅ Commands router loaded")
        except Exception as e:
            print(f"❌ Commands router failed: {e}")
        
        print("✅ All routers loaded successfully!")
        print("🤖 Bot is starting polling...")
        
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🐍 Python version:", sys.version)
    asyncio.run(main())