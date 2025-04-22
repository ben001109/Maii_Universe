import logging
from discord.ext import commands
from discord import app_commands
import discord
from database import claim_daily

logger = logging.getLogger(__name__)

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="每日簽到領錢！")
    async def daily(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = claim_daily(player_id)

        if success:
            logger.info(f"{interaction.user.name} 使用 /daily 成功：{message}")
        else:
            logger.warning(f"{interaction.user.name} 使用 /daily 失敗：{message}")

        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Daily(bot))