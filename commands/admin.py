from discord.ext import commands
from discord import app_commands
import discord
import logging
from database import inject_money, upgrade_all, reset_player, simulate_hourly_income
from utils.Auth import is_admin

logger = logging.getLogger(__name__)

class Admin(commands.GroupCog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not is_admin(interaction.user.id):
            await interaction.response.send_message("⛔ 你沒有權限使用這個指令。", ephemeral=True)
            return False
        return True

    @app_commands.command(name="sync", description="🔄 重新同步 Slash 指令（管理員專用）")
    async def sync_cmd(self, interaction: discord.Interaction):
        from utils.CommandSync import full_sync
        await full_sync(self.bot)
        await interaction.response.send_message("✅ 指令已重新同步完成（Guild + Global）", ephemeral=True)

    @app_commands.command(name="inject_money", description="給自己加錢（測試用）")
    @app_commands.describe(amount="要加多少美金？")
    async def inject_money_cmd(self, interaction: discord.Interaction, amount: float):
        player_id = str(interaction.user.id)
        inject_money(player_id, amount)
        logger.info(f"[ADMIN] {interaction.user.name} 注入 ${amount:.2f}")
        await interaction.response.send_message(f"💵 成功注入 ${amount:.2f}！")

    @app_commands.command(name="upgrade_all", description="升級所有項目到 Lv.5（測試用）")
    async def upgrade_all_cmd(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        upgrade_all(player_id)
        logger.info(f"[ADMIN] {interaction.user.name} 將所有升級提升至 Lv.5")
        await interaction.response.send_message("📈 所有升級已提升至 Lv.5！")

    @app_commands.command(name="reset", description="重設自己的企業資料（測試用）")
    async def reset_cmd(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        reset_player(player_id)
        logger.info(f"[ADMIN] {interaction.user.name} 重設企業資料")
        await interaction.response.send_message("🗑️ 你的企業資料已重置。")

    @app_commands.command(name="simulate_hour", description="模擬 1 小時排程收入（測試用）")
    async def simulate_hour_cmd(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        reward = simulate_hourly_income(player_id)
        logger.info(f"[ADMIN] {interaction.user.name} 模擬獲得 ${reward:.2f} 排程收入")
        await interaction.response.send_message(f"⏱️ 模擬排程完成，獲得 ${reward:.2f}！")

async def setup(bot):
    await bot.add_cog(Admin(bot))