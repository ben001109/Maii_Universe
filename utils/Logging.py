import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_folder="logs", log_file="bot.log"):
    os.makedirs(log_folder, exist_ok=True)
    handler = RotatingFileHandler(f"{log_folder}/{log_file}", maxBytes=1_000_000, backupCount=5, encoding="utf-8")
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s",
        handlers=[handler, logging.StreamHandler()]
    )

def log_command(user, command_name, message=None, level="info"):
    logger = logging.getLogger("MaiiBot")
    content = f"{user} 使用 /{command_name}" + (f" ｜{message}" if message else "")
    if level == "warning":
        logger.warning(content)
    elif level == "error":
        logger.error(content)
    else:
        logger.info(content)
