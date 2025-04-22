from discord.ext import commands
from discord import app_commands
import discord
import logging
logger = logging.getLogger(__name__)

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = bot

    @app_commands.command(name="ping", description="看看我醒著沒？（回報延遲）")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.app.latency * 1000)
        await interaction.response.send_message(f"🏓 pong！我醒著喔，現在的延遲是：{latency_ms}ms")

async def setup(bot):
    await bot.add_cog(Ping(bot))
