from discord.ext import commands
from discord import app_commands
import discord
from database import get_player, update_industry_name, get_all_players, upgrade_industry
import logging
logger = logging.getLogger(__name__)

class Industry(commands.GroupCog, name="industry"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create", description="建立你自己的企業名稱")
    @app_commands.describe(name="你要為企業取什麼名字呢？")
    async def create_industry(self, interaction: discord.Interaction, name: str):
        player_id = str(interaction.user.id)
        player = get_player(player_id)
        if not player:
            await interaction.response.send_message("⚠️ 你還沒創建帳號喔，請先用 `/start`！")
            return
        update_industry_name(player_id, name)
        await interaction.response.send_message(f"🏢 你成功將企業命名為：**{name}**！使用 `/profile` 查看更新！")

    @app_commands.command(name="list", description="查看所有企業列表")
    async def list_industries(self, interaction: discord.Interaction):
        players = get_all_players()
        if not players:
            await interaction.response.send_message("⚠️ 目前尚無任何企業資料。")
            return
        lines = [f"🏢 {p['industry']} ｜👤 {p['name']}" for p in players]
        await interaction.response.send_message(f"```所有企業列表：\n{chr(10).join(lines)}```")

    @app_commands.command(name="upgrade", description="升級你的企業等級（提升收入）")
    async def upgrade_industry_command(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = upgrade_industry(player_id)
        logger.info(f"{interaction.user.name} 使用 /industry upgrade ｜{message}")
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Industry(bot))
