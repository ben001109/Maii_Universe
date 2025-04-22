import os
import logging

logger = logging.getLogger(__name__)

async def load_slash_command_modules(bot, commands_folder="commands"):
    count = 0
    for filename in os.listdir(commands_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_path = f"{commands_folder.replace('/', '.')}.{filename[:-3]}"
            try:
                await bot.load_extension(module_path)
                logger.info(f"✅ 已載入模組：{module_path}")
                count += 1
            except Exception as e:
                logger.warning(f"❌ 模組載入失敗：{module_path}，錯誤：{e}")
    return count
