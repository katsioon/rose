"""
Advanced Discord Bot - Main Entry Point
A comprehensive Discord bot with gaming, moderation, movies, weather, news, music, and economy.
"""

import os
import logging
from pathlib import Path
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
Path('logs').mkdir(exist_ok=True)

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')
ACTIVITY_STATUS = "🎮 Gaming | 🎵 Music | 📺 Movies"

class AdvancedDiscordBot(commands.Bot):
    """Advanced Discord Bot with multiple features"""
    
    def __init__(self):
        intents = disnake.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.guild_messages = True
        intents.direct_messages = True
        
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None,
            activity=disnake.Activity(
                type=disnake.ActivityType.playing,
                name=ACTIVITY_STATUS
            )
        )
        
        self.start_time = datetime.now()
        self.synced = False
        self.db_connected = False
        
    async def on_ready(self):
        """Called when bot is ready"""
        if not self.synced:
            await self.sync_commands()
            self.synced = True
        
        logger.info(f'✅ Bot is online as {self.user}')
        logger.info(f'📊 Connected to {len(self.guilds)} guilds')
        logger.info(f'👥 Total users: {sum(g.member_count for g in self.guilds)}')
        
        # Start background tasks
        await self.start_background_tasks()
    
    async def start_background_tasks(self):
        """Start background tasks for 24/7 operation"""
        asyncio.create_task(self.heartbeat_monitor())
        asyncio.create_task(self.periodic_activity_update())
    
    async def heartbeat_monitor(self):
        """Monitor bot heartbeat"""
        while not self.is_closed():
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                logger.info(f"💓 Heartbeat - Latency: {self.latency*1000:.2f}ms")
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
    
    async def periodic_activity_update(self):
        """Update activity status periodically"""
        activities = [
            "🎮 Gaming | 🎵 Music",
            "🎬 Movies | 📡 News",
            "⛅ Weather | 💰 Economy",
            "🛡️ Moderation | 🔧 Config"
        ]
        index = 0
        
        while not self.is_closed():
            try:
                await self.change_presence(
                    activity=disnake.Activity(
                        type=disnake.ActivityType.playing,
                        name=activities[index % len(activities)]
                    )
                )
                index += 1
                await asyncio.sleep(300)  # Change every 5 minutes
            except Exception as e:
                logger.error(f"Activity update error: {e}")
    
    async def load_cogs(self):
        """Load all cogs from cogs directory"""
        cogs_dir = Path('cogs')
        cogs_dir.mkdir(exist_ok=True)
        
        cog_count = 0
        for cog_file in cogs_dir.glob('*.py'):
            if cog_file.name.startswith('_'):
                continue
            
            cog_name = cog_file.stem
            try:
                await self.load_extension(f'cogs.{cog_name}')
                logger.info(f'✅ Loaded cog: {cog_name}')
                cog_count += 1
            except Exception as e:
                logger.error(f'❌ Failed to load cog {cog_name}: {e}')
        
        logger.info(f'📦 Total cogs loaded: {cog_count}')
    
    async def on_error(self, event_method, *args, **kwargs):
        """Handle errors globally"""
        logger.error(f'Error in {event_method}:', exc_info=True)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have permission to do that.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing argument: {error.param}")
        else:
            logger.error(f'Command error: {error}')


async def main():
    """Main function to start the bot"""
    bot = AdvancedDiscordBot()
    
    async with bot:
        # Load all cogs before connecting
        await bot.load_cogs()
        
        try:
            await bot.start(DISCORD_TOKEN)
        except KeyboardInterrupt:
            logger.info("Bot shutdown initiated by user")
        except Exception as e:
            logger.error(f"Critical error: {e}")
            raise


if __name__ == '__main__':
    if not DISCORD_TOKEN:
        logger.error("❌ DISCORD_TOKEN not found in .env file")
        exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
