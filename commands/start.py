from discord.ext import commands
from discord import app_commands
import discord
from database import register_player
import logging
logger = logging.getLogger(__name__)

from discord.ext import commands
from discord import app_commands
import discord

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="start", description="開始你的企業人生！")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎉 你已經創建了企業！")

async def setup(bot):
    await bot.add_cog(Start(bot))

