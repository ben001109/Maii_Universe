from discord.ext import commands
from discord import app_commands
import discord
import logging
from database import (
    inject_money,
    upgrade_all,
    reset_player
)
from utils.Experience import simulate_hourly_income
from utils.Auth import is_admin
from utils.CommandSync import full_sync

logger = logging.getLogger(__name__)

class Admin(commands.GroupCog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not is_admin(interaction.user.id):
            await interaction.response.send_message("⛔ 你沒有權限使用這個指令。", ephemeral=True)
            return False
        return True

    @app_commands.command(name="sync", description="🔄 重新同步 Slash 指令（僅限 Guild）")
    async def sync_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await full_sync(self.bot)
        await interaction.followup.send("✅ 指令已重新同步完成（Guild）", ephemeral=True)

    @app_commands.command(name="inject_money", description="💰 管理員加錢")
    @app_commands.describe(amount="要加多少錢？")
    async def inject_money_cmd(self, interaction: discord.Interaction, amount: float):
        await interaction.response.defer(ephemeral=True)
        if inject_money(str(interaction.user.id), amount):
            await interaction.followup.send(f"✅ 成功加了 ${amount}", ephemeral=True)
        else:
            await interaction.followup.send("⚠️ 找不到玩家資料", ephemeral=True)

    @app_commands.command(name="reset", description="🗑️ 重設玩家資料")
    @app_commands.describe(user="要重設的對象（預設為自己）")
    async def reset_cmd(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        target = user or interaction.user
        reset_player(str(target.id))
        await interaction.followup.send(f"🧹 {target.display_name} 的企業資料已重設", ephemeral=True)

    @app_commands.command(name="simulate_hour", description="⏱️ 模擬一小時收入")
    async def simulate_hour_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        earned = simulate_hourly_income(str(interaction.user.id))
        await interaction.followup.send(f"💵 獲得模擬收入：${earned:.2f}", ephemeral=True)

    @app_commands.command(name="upgrade_all", description="📈 全部升級至 Lv.5")
    async def upgrade_all_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        upgrade_all(str(interaction.user.id))
        await interaction.followup.send("📊 所有項目已升級至 Lv.5", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
