from discord.ext import commands
from discord import app_commands
import discord
from database import get_player
import logging
logger = logging.getLogger(__name__)

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="查看你的企業目前狀態")
    async def status(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = get_player(player_id)

        if not player:
            await interaction.response.send_message("⚠️ 你還沒有創建企業喔，請先使用 `/start`")
            return

        name = player["name"]
        industry = player["industry"]
        money = player["money"]
        level = player["level"]
        items = player.get("items", [])
        item_list = "\n".join([f"🔹 {item}" for item in items]) if items else "（尚未購買任何商品）"
        logger.info(f"{interaction.user.name} 使用 /status")
        msg = f"""```yaml
🪪 玩家名稱：{name}
🏢 企業名稱：{industry}
💰 資金：${money}
📈 等級：Lv.{level}
📦 擁有商品：
{item_list}
```"""

        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Status(bot))