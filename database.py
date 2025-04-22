from datetime import datetime, timedelta

_players = {}

def register_player(player_id, name):
    if player_id in _players:
        return False
    _players[player_id] = {
        "name": name,
        "industry": "麥麥食堂",
        "money": 3200,
        "last_daily_claim": None,
        "last_work_time": None,  # ⬅ 新增欄位
        "level": 1,
        "items": []
    }
    return True


def get_player(player_id):
    return _players.get(player_id)

def update_industry_name(player_id, new_name):
    if player_id in _players:
        _players[player_id]["industry"] = new_name
        return True
    return False

def get_all_players():
    return _players.values()

def claim_daily(player_id):
    from datetime import datetime, timedelta

    player = _players.get(player_id)
    if not player:
        return False, "你還沒有創建企業喔！"

    now = datetime.now()
    last = player.get("last_daily_claim")

    if last is not None:
        last_time = datetime.fromisoformat(last)
        if now.date() == last_time.date():
            return False, f"你今天已經簽到過囉！上次簽到時間：{last_time.strftime('%Y-%m-%d %H:%M:%S')}"

    player["money"] += 500  # 發錢
    player["last_daily_claim"] = now.isoformat()
    return True, f"✅ 簽到成功，獲得 $500！目前資金：${player['money']}"

def upgrade_industry(player_id):
    player = _players.get(player_id)
    if not player:
        return False, "你尚未創建企業！"

    current_level = player.get("level", 1)
    cost = current_level * 1000

    if player["money"] < cost:
        return False, f"❌ 升級失敗：你需要 ${cost}，但目前只有 ${player['money']}"

    player["money"] -= cost
    player["level"] += 1
    return True, f"✅ 升級成功！現在是 Lv.{player['level']}，剩餘資金：${player['money']}"

ITEMS = {
    "麥麥旗幟": {"price": 1000, "description": "代表麥宇宙精神的招牌旗幟"},
    "點餐機": {"price": 2500, "description": "讓顧客更有效率地點餐"},
    "超級鍋爐": {"price": 5000, "description": "可煮更多拉麵！提升效率"},
}

def get_market_items():
    return ITEMS

def buy_item(player_id, item_name):
    player = _players.get(player_id)
    if not player:
        return False, "❌ 你尚未建立企業！請先使用 `/start`"

    item = ITEMS.get(item_name)
    if not item:
        return False, "❌ 商品不存在，請檢查拼字"

    if item_name in player["items"]:
        return False, "⚠️ 你已經擁有這個商品了！"

    if player["money"] < item["price"]:
        return False, f"❌ 你沒有足夠的資金來購買 {item_name}（需要 ${item['price']}）"

    player["money"] -= item["price"]
    player["items"].append(item_name)
    return True, f"✅ 成功購買 **{item_name}**！目前剩餘資金：${player['money']}"

def work_with_cooldown(player_id):
    player = _players.get(player_id)
    if not player:
        return False, "⚠️ 尚未建立企業！"

    upgrades = player.get("upgrades", {"equipment": 0, "operation": 0})
    equipment_level = upgrades.get("equipment", 0)
    operation_level = upgrades.get("operation", 0)

    base_cooldown = 60  # 分鐘
    cooldown_reduction = min(operation_level * 5, 45)  # 最多減 45 分鐘
    cooldown_minutes = max(15, base_cooldown - cooldown_reduction)

    now = datetime.now()
    last_time_str = player.get("last_work_time")
    if last_time_str:
        last_time = datetime.fromisoformat(last_time_str)
        next_available_time = last_time + timedelta(minutes=cooldown_minutes)
        if now < next_available_time:
            remain = next_available_time - now
            minutes = int(remain.total_seconds() // 60)
            seconds = int(remain.total_seconds() % 60)
            return False, f"🕒 你太拼了啦～請休息一下！剩下 {minutes} 分 {seconds} 秒後再試一次吧！"

    # 成功工作，發錢
    reward = 100 + equipment_level * 50
    player["money"] += reward
    player["last_work_time"] = now.isoformat()
    return True, f"💼 工作完成！你獲得了 ${reward:.2f}。目前資金：${player['money']:.2f}"

def upgrade_category(player_id, category):
    player = _players.get(player_id)
    if not player:
        return False, "⚠️ 尚未註冊企業。請先使用 `/start`"

    if "upgrades" not in player:
        player["upgrades"] = {"equipment": 0, "operation": 0, "decoration": 0}

    if category not in player["upgrades"]:
        return False, "❌ 無效的升級類別！"

    current_level = player["upgrades"][category]

    cost_map = {
        "equipment": 1500,
        "operation": 1200,
        "decoration": 1000
    }

    cost = cost_map[category] * (current_level + 1)
    if player["money"] < cost:
        return False, f"❌ 升級失敗！你需要 ${cost:.2f}，但你只有 ${player['money']:.2f}"

    player["money"] -= cost
    player["upgrades"][category] += 1

    return True, f"✅ 你成功將 `{category}` 升級到 Lv.{player['upgrades'][category]}，消耗 ${cost:.2f}！剩餘資金：${player['money']:.2f}"

def inject_money(player_id, amount):
    player = _players.get(player_id)
    if player:
        player["money"] += amount

def upgrade_all(player_id):
    player = _players.get(player_id)
    if player:
        if "upgrades" not in player:
            player["upgrades"] = {"equipment": 0, "operation": 0, "decoration": 0}
        for k in player["upgrades"]:
            player["upgrades"][k] = 5

def reset_player(player_id):
    if player_id in _players:
        del _players[player_id]

def simulate_hourly_income(player_id):
    player = _players.get(player_id)
    if not player:
        return 0.0

    upgrades = player.get("upgrades", {})
    income = (
        upgrades.get("equipment", 0) * 200 +
        upgrades.get("operation", 0) * 150 +
        upgrades.get("decoration", 0) * 100
    )
    player["money"] += income
    return income