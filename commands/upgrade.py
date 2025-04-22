from discord.ext import commands
from discord import app_commands
import discord
from database import upgrade_category
import logging

logger = logging.getLogger(__name__)

class Upgrade(commands.GroupCog, name="upgrade"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="equipment", description="升級設備：提升廚具、自動化產能")
    async def upgrade_equipment(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = upgrade_category(player_id, "equipment")
        logger.info(f"{interaction.user.name} 使用 /upgrade equipment：{message}")
        await interaction.response.send_message(message)

    @app_commands.command(name="operation", description="升級營運：提升客戶處理、外送能力")
    async def upgrade_operation(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = upgrade_category(player_id, "operation")
        logger.info(f"{interaction.user.name} 使用 /upgrade operation：{message}")
        await interaction.response.send_message(message)

    @app_commands.command(name="decoration", description="升級裝潢：提升吸引力、顧客流量")
    async def upgrade_decoration(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        success, message = upgrade_category(player_id, "decoration")
        logger.info(f"{interaction.user.name} 使用 /upgrade decoration：{message}")
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Upgrade(bot))
