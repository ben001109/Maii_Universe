from discord.ext import commands
from discord import app_commands
import discord
from database import get_player
from ascii_ui import generate_profile_ui
import logging
logger = logging.getLogger(__name__)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="查看你的企業檔案")
    async def profile(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = get_player(player_id)
        if player:
            ui = generate_profile_ui(player["name"], player["industry"], player["money"])
            await interaction.response.send_message(f"```{ui}```")
        else:
            await interaction.response.send_message("⚠️ 你還沒有創建企業！請先使用 `/start`")

async def setup(bot):
    await bot.add_cog(Profile(bot))
