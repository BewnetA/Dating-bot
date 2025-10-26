import asyncio
import logging
import time
import sys
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

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
        
    async def on_startup(self, bot: Bot):
        """Actions to perform on bot startup"""
        print("🤖 Ethiopia Connect Bot Starting with Webhook...")
        print("📊 Database initialized:", config.DB_NAME)
        
        # Set webhook
        webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
        await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True
        )
        print(f"✅ Webhook set to: {webhook_url}")
        
    async def on_shutdown(self, bot: Bot):
        """Actions to perform on bot shutdown"""
        print("🛑 Bot is shutting down...")
        await bot.delete_webhook()
        print("✅ Webhook deleted")
        
    async def setup_bot(self):
        """Setup bot with webhook configuration"""
        try:
            # Initialize bot and dispatcher
            bot = Bot(token=config.BOT_TOKEN)
            dp = Dispatcher()
            
            # Register startup and shutdown handlers
            dp.startup.register(self.on_startup)
            dp.shutdown.register(self.on_shutdown)
            
            # Include routers
            print("🔄 Loading routers...")
            dp.include_router(start_router)
            dp.include_router(profile_router)
            dp.include_router(matching_router)
            dp.include_router(commands_router)
            print("✅ All routers loaded!")
            
            # Create aiohttp application
            app = web.Application()
            webhook_requests_handler = SimpleRequestHandler(
                dispatcher=dp,
                bot=bot,
            )
            
            # Register webhook handler
            webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)
            setup_application(app, dp, bot=bot)
            
            return app, bot
            
        except Exception as e:
            print(f"❌ Bot setup failed: {e}")
            logging.error(f"Bot setup error: {e}", exc_info=True)
            raise
            
    async def run_webhook(self):
        """Run the bot with webhook"""
        try:
            app, bot = await self.setup_bot()
            
            # Start web server
            runner = web.AppRunner(app)
            await runner.setup()
            
            site = web.TCPSite(
                runner, 
                host=config.WEBAPP_HOST, 
                port=config.WEBAPP_PORT
            )
            
            await site.start()
            print(f"🚀 Webhook server started on {config.WEBAPP_HOST}:{config.WEBAPP_PORT}")
            print("📝 Bot is ready to receive updates via webhook!")
            
            # Run forever
            await asyncio.Future()  # run forever
            
        except KeyboardInterrupt:
            print("⏹️ Bot stopped by user")
            return False
        except Exception as e:
            print(f"❌ Webhook bot crashed with error: {e}")
            logging.error(f"Webhook bot crash: {e}", exc_info=True)
            return True
            
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
            
            should_restart = await self.run_webhook()
            
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