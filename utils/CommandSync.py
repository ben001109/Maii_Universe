import discord
import logging
import asyncio
import time

logger = logging.getLogger("MaiiBot")

async def sync_global_commands(bot: discord.Client):
    """
    同步 Global (全域) Slash 指令（含 timeout 與耗時紀錄）
    """
    try:
        start = time.time()
        synced = await asyncio.wait_for(bot.tree.sync(), timeout=15.0)
        elapsed = time.time() - start
        logger.info(f"🌐 已同步 {len(synced)} 個 Global Slash 指令，耗時 {elapsed:.2f}s")
    except asyncio.TimeoutError:
        logger.warning("⚠️ 同步 Global Slash 指令超時（可能是 Discord API 回應過慢）")
    except Exception as e:
        logger.error(f"❌ 同步 Global Slash 指令失敗：{e}")

async def sync_guild_commands(bot: discord.Client, guild: discord.Guild):
    """
    同步指定 Guild 的 Slash 指令
    """
    synced = await bot.tree.sync(guild=discord.Object(id=guild.id))
    logger.info(f"👥 已同步 {len(synced)} 個指令到 Guild: {guild.name} ({guild.id})")

async def clear_guild_commands(bot: discord.Client, guild: discord.Guild):
    """
    清除指定 Guild 的 Slash 指令
    """
    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)
    logger.info(f"❌ 已清除並重建 Guild 指令：{guild.name} ({guild.id})")

async def full_sync(bot: discord.Client):
    """
    啟動時：重新同步 Global + 清除並重建所有 Guild 的指令
    """
    await sync_global_commands(bot)

    for guild in bot.guilds:
        await clear_guild_commands(bot, guild)
        await sync_guild_commands(bot, guild)

    logger.info(f"🌌 完成所有 Guild + Global 的 Slash 指令同步！")