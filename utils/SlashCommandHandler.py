import os
import logging

logger = logging.getLogger(__name__)

async def load_slash_command_modules(bot, commands_folder="commands"):
    count = 0
    for filename in os.listdir(commands_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_path = f"commands.{filename[:-3]}"  # ✅ 正確的 Python 模組路徑
            try:
                await bot.load_extension(module_path)
                logging.getLogger(__name__).info(f"✅ 已載入模組：{module_path}")
                count += 1
            except Exception as e:
                logging.getLogger(__name__).warning(f"❌ 模組載入失敗：{module_path}，錯誤：{e}")
    return count