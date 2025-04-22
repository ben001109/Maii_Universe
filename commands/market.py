from discord.ext import commands
from discord import app_commands
import discord
from database import get_market_items, buy_item
import logging
logger = logging.getLogger(__name__)

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /market_show
    @app_commands.command(name="market_show", description="查看目前販售中的商品")
    async def market_show(self, interaction: discord.Interaction):
        items = get_market_items()
        lines = ["🛍️ **商品清單：**"]
        for name, data in items.items():
            lines.append(f"📦 {name} - ${data['price']}\n  📘 {data['description']}")
        await interaction.response.send_message("\n".join(lines))

    # /market_buy
    @app_commands.command(name="market_buy", description="購買一個商品（消耗資金）")
    @app_commands.describe(item="商品名稱，請參考 /market_show")
    async def market_buy(self, interaction: discord.Interaction, item: str):
        player_id = str(interaction.user.id)
        success, message = buy_item(player_id, item)
        if success:
            logger.info(f"{interaction.user.name} 購買成功：{item} ｜{message}")
        else:
            logger.warning(f"{interaction.user.name} 購買失敗：{item} ｜{message}")
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Market(bot))
