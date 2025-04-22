from discord.ext import commands
from discord import app_commands
import discord
from database import get_player

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="查看企業模擬資訊")
    async def status(self, interaction: discord.Interaction):
        player = get_player(str(interaction.user.id))
        if not player:
            await interaction.response.send_message("⚠️ 尚未註冊，請使用 `/start`")
            return

        message = (
            f"🏢 企業名稱：{player['industry']}\n"
            f"💼 等級：Lv.{player['level']} ｜ EXP：{player['exp']}\n"
            f"⚙️ 設備：Lv.{player['equipment']}\n"
            f"📦 營運：Lv.{player['operation']}\n"
            f"🌟 裝潢：Lv.{player['decoration']}\n"
        )
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Status(bot))
