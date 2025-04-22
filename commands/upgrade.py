from discord.ext import commands
from discord import app_commands
import discord
from database import get_player, update_player
import logging

logger = logging.getLogger(__name__)

class Upgrade(commands.GroupCog, name="upgrade"):
    def __init__(self, bot):
        self.bot = bot

    def upgrade_category(self, player, category):
        cost = (player[category] + 1) * 300
        if player["money"] < cost:
            return False, f"💸 升級失敗，資金不足（需要 ${cost}）"
        player["money"] -= cost
        player[category] += 1
        update_player(player)
        return True, f"📈 成功升級 {category} 至 Lv.{player[category]}，消耗 ${cost}"

    @app_commands.command(name="equipment", description="升級設備：提升產能")
    async def upgrade_equipment(self, interaction: discord.Interaction):
        player = get_player(str(interaction.user.id))
        success, msg = self.upgrade_category(player, "equipment")
        await interaction.response.send_message(msg)

    @app_commands.command(name="operation", description="升級營運：縮短工作冷卻")
    async def upgrade_operation(self, interaction: discord.Interaction):
        player = get_player(str(interaction.user.id))
        success, msg = self.upgrade_category(player, "operation")
        await interaction.response.send_message(msg)

    @app_commands.command(name="decoration", description="升級裝潢：提升客流")
    async def upgrade_decoration(self, interaction: discord.Interaction):
        player = get_player(str(interaction.user.id))
        success, msg = self.upgrade_category(player, "decoration")
        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Upgrade(bot))
