from discord.ext import commands
from discord import app_commands
import discord
from database import get_player, get_visible_fields
from ascii_ui import generate_profile_ui

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="查看自己的企業資料，或 @tag 他人查詢")
    @app_commands.describe(user="你要查詢的對象（留空 = 查自己）")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        viewer_id = str(interaction.user.id)
        target_user = user or interaction.user
        target_id = str(target_user.id)

        target = get_player(target_id)
        if not target:
            await interaction.response.send_message("⚠️ 查無企業資料。")
            return

        is_self = viewer_id == target_id
        visible = set(get_visible_fields(target_id)) if not is_self else None

        def safe_show(key, value):
            return value if is_self or (visible and key in visible) else "🔒 保密"

        lines = [
            f"🪪 **{target_user.display_name} 的企業資料**",
            f"👤 名稱：{safe_show('name', target['name'])}",
            f"🏢 企業：{safe_show('industry', target['industry'])}",
        ]

        if is_self or 'money' in visible:
            lines.append(f"💰 資金：{safe_show('money', f'${target['money']:.2f}')}")

        if is_self or 'level' in visible:
            lines.append(f"📈 等級：{safe_show('level', f'Lv.{target['level']}')}")

        if is_self or 'equipment' in visible:
            lines.append(f"⚙️ 設備：{safe_show('equipment', f'Lv.{target['equipment']}')}")

        if is_self or 'operation' in visible:
            lines.append(f"📦 營運：{safe_show('operation', f'Lv.{target['operation']}')}")

        if is_self or 'decoration' in visible:
            lines.append(f"🌟 裝潢：{safe_show('decoration', f'Lv.{target['decoration']}')}")

        message = "\n".join(lines)
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Profile(bot))
