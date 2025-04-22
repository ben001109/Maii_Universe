from discord.ext import commands
from discord import app_commands
import discord
from database import get_player, update_player
from utils.Experience import gain_exp
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="work", description="努力工作賺點錢！（冷卻時間依營運等級縮短）")
    async def work(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = get_player(player_id)

        if not player:
            await interaction.response.send_message("⚠️ 你尚未創建企業！請使用 `/start`。")
            return

        now = datetime.now()
        last_work_time = player.get("last_work")
        if last_work_time:
            last_time = datetime.fromisoformat(last_work_time)
            cooldown = max(60 - (player["operation"] * 5), 10)
            if (now - last_time) < timedelta(seconds=cooldown):
                remain = cooldown - (now - last_time).seconds
                await interaction.response.send_message(f"🕒 冷卻中，請在 {remain} 秒後再試。")
                return

        income = 100 + player["equipment"] * 20
        player["money"] += income
        player["last_work"] = now.isoformat()
        update_player(player)

        gain_exp(player_id, 30)
        logger.info(f"{interaction.user.name} 使用 /work 賺取 ${income}")
        await interaction.response.send_message(f"💼 工作成功，賺取 ${income}！")

async def setup(bot):
    await bot.add_cog(Work(bot))
