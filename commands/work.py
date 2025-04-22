from discord.ext import commands
from discord import app_commands
import discord
from database import work_with_cooldown
import logging

logger = logging.getLogger(__name__)

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="work", description="努力工作賺點錢！（冷卻時間依營運等級縮短）")
    async def work(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = work_with_cooldown(player_id)

        if success:
            logger.info(f"{interaction.user.name} 使用 /work 成功：{message}")
        else:
            logger.warning(f"{interaction.user.name} 使用 /work 失敗：{message}")

        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Work(bot))
