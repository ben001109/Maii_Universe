from config import ADMIN_IDS
import logging

logger = logging.getLogger("MaiiBot")

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def print_admins(bot):
    print("🔐 已載入管理員：")
    for admin_id in ADMIN_IDS:
        user = bot.get_user(admin_id)
        label = f"{user} ({admin_id})" if user else f"未知使用者 ({admin_id})"
        print(f"   👉 {label}")
        logger.info(f"👉 管理員：{label}")
