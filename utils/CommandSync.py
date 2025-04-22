import discord
import logging

logger = logging.getLogger("MaiiBot")

async def sync_guild_commands(bot: discord.Client, guild: discord.Guild):
    synced = await bot.tree.sync(guild=discord.Object(id=guild.id))
    logger.info(f"👥 已同步 {len(synced)} 個指令到 Guild: {guild.name} ({guild.id})")

async def clear_guild_commands(bot: discord.Client, guild: discord.Guild):
    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)
    logger.info(f"🧹 已清除並重建 Guild 指令：{guild.name} ({guild.id})")

async def full_sync(bot: discord.Client):
    """
    ✅ 僅清除並同步 Guild 指令，避免 Discord 上出現「重複 Slash 指令」問題
    """
    for guild in bot.guilds:
        await clear_guild_commands(bot, guild)
        await sync_guild_commands(bot, guild)
    logger.info(f"🌌 所有 Guild Slash 指令已同步完成")
