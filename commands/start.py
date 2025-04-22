from discord.ext import commands
from discord import app_commands
import discord
from database import register_player, get_player
import logging

logger = logging.getLogger(__name__)

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="start", description="開始你的企業人生！")
    async def start(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player_name = interaction.user.name

        if get_player(player_id):
            await interaction.response.send_message("⚠️ 你已經建立過企業囉，請使用 `/profile` 查看！", ephemeral=True)
            return

        register_player(player_id, player_name)
        logger.info(f"[START] 建立新玩家：{player_name} ({player_id})")
        await interaction.response.send_message("🎉 企業創立成功！歡迎加入麥宇宙計畫 🚀", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Start(bot))
