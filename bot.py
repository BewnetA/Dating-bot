import asyncio
import logging
import time
import sys
from aiogram import Bot, Dispatcher

from config import config
from database import db

# Import handlers
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.matching import router as matching_router
from handlers.commands import router as commands_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class BotManager:
    def __init__(self):
        self.max_restarts = 10
        self.restart_delay = 5  # seconds
        self.restart_count = 0
        self.last_restart = 0
        
    async def run_bot(self):
        """Run the bot with error handling"""
        print("🤖 Ethiopia Connect Bot Starting...")
        print("📊 Database initialized:", config.DB_NAME)
        
        try:
            # Initialize bot
            bot = Bot(token=config.BOT_TOKEN)
            dp = Dispatcher()
            
            # Include routers
            print("🔄 Loading routers...")
            dp.include_router(start_router)
            dp.include_router(profile_router)
            dp.include_router(matching_router)
            dp.include_router(commands_router)
            print("✅ All routers loaded!")
            
            # Start polling with error handling
            print("🚀 Bot is starting polling...")
            await dp.start_polling(bot)
            
        except KeyboardInterrupt:
            print("⏹️ Bot stopped by user")
            return False  # Don't restart on user interrupt
        except Exception as e:
            print(f"❌ Bot crashed with error: {e}")
            logging.error(f"Bot crash: {e}", exc_info=True)
            return True  # Signal to restart
            
    async def start_with_restart(self):
        """Main loop with auto-restart capability"""
        while self.restart_count < self.max_restarts:
            current_time = time.time()
            
            # Rate limiting for restarts
            if current_time - self.last_restart < self.restart_delay:
                await asyncio.sleep(self.restart_delay)
                
            self.last_restart = current_time
            self.restart_count += 1
            
            print(f"🔄 Attempt {self.restart_count}/{self.max_restarts} to start bot...")
            
            should_restart = await self.run_bot()
            
            if not should_restart:
                break  # Exit loop if we shouldn't restart
                
            if self.restart_count < self.max_restarts:
                print(f"⏰ Restarting in {self.restart_delay} seconds...")
                await asyncio.sleep(self.restart_delay)
            else:
                print("🚫 Maximum restart attempts reached. Giving up.")
                break

async def main():
    bot_manager = BotManager()
    await bot_manager.start_with_restart()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹️ Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()