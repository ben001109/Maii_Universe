from discord.ext import commands
from discord import app_commands
import discord

# 假設未來擴充用，你可以將商品儲存在資料庫或 JSON

def get_market_items():
    return {
        "自動麵包機": {"price": 300, "description": "每日自動生產金幣 🍞"},
        "舒適沙發": {"price": 150, "description": "提升顧客停留率 🛋️"},
    }

class Market(commands.GroupCog, name="market"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show", description="查看販售商品")
    async def show(self, interaction: discord.Interaction):
        items = get_market_items()
        lines = [f"📦 {name} - ${data['price']}\n　📘 {data['description']}" for name, data in items.items()]
        await interaction.response.send_message("🛍️ **商品清單：**\n" + "\n".join(lines))

async def setup(bot):
    await bot.add_cog(Market(bot))
