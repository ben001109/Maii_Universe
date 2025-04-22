import discord
from discord.ext import commands
import logging
from config import TOKEN
from utils.Logging import setup_logging
from utils.SlashCommandHandler import load_slash_command_modules
from utils.Auth import print_admins
from utils.CommandSync import full_sync
from database import init_db

setup_logging()
init_db()
logger = logging.getLogger("MaiiBot")

class MaiiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

bot = MaiiBot()

@bot.event
async def on_ready():
    await load_slash_command_modules(bot)
    await full_sync(bot)
    print(f"🟢 Bot 上線：{bot.user}｜伺服器數量：{len(bot.guilds)}")
    await print_admins(bot)

bot.run(TOKEN)
