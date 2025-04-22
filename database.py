import os
import sqlite3
import json
from datetime import datetime, timedelta
from utils.PlayerFactory import get_default_player

DB_FOLDER = "data"
DB_FILE = f"{DB_FOLDER}/maii.db"

def init_db():
    os.makedirs(DB_FOLDER, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id TEXT PRIMARY KEY,
            name TEXT,
            industry TEXT,
            money REAL,
            exp INTEGER,
            level INTEGER,
            equipment INTEGER,
            operation INTEGER,
            decoration INTEGER,
            last_daily TEXT,
            last_work TEXT,
            visible_fields TEXT DEFAULT '["name", "industry", "level"]'
        )
        """)
        conn.commit()

def register_player(player_id, name):
    if get_player(player_id):
        return False
    player = get_default_player(player_id, name)
    visible_fields = json.dumps(["name", "industry", "level"])
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO players (id, name, industry, money, exp, level, equipment, operation, decoration, last_daily, last_work, visible_fields)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player["id"], player["name"], player["industry"], player["money"], player["exp"],
            player["level"], player["equipment"], player["operation"], player["decoration"],
            player["last_daily"], player["last_work"], visible_fields
        ))
        conn.commit()
    return True

def get_player(player_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_player(player):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE players
        SET name=?, industry=?, money=?, exp=?, level=?,
            equipment=?, operation=?, decoration=?,
            last_daily=?, last_work=?, visible_fields=?
        WHERE id=?
        """, (
            player["name"], player["industry"], player["money"], player["exp"], player["level"],
            player["equipment"], player["operation"], player["decoration"],
            player["last_daily"], player["last_work"],
            player.get("visible_fields", json.dumps(["name", "industry", "level"])),
            player["id"]
        ))
        conn.commit()

# === 隱私系統功能 ===

def get_visible_fields(player_id):
    player = get_player(player_id)
    if not player:
        return []
    try:
        return json.loads(player["visible_fields"])
    except Exception:
        return []

def update_visible_fields(player_id, fields: list):
    player = get_player(player_id)
    if not player:
        return False
    player["visible_fields"] = json.dumps(fields)
    update_player(player)
    return True

# === 管理員與企業功能 ===

def inject_money(player_id: str, amount: float) -> bool:
    player = get_player(player_id)
    if not player:
        return False
    player["money"] += amount
    update_player(player)
    return True

def reset_player(player_id: str):
    player = get_player(player_id)
    if not player:
        return
    reset_data = get_default_player(player_id, player["name"])
    update_player(reset_data)

def upgrade_industry(player_id: str, field: str = "equipment") -> (bool, str):
    player = get_player(player_id)
    if not player:
        return False, "⚠️ 找不到玩家資料"
    cost = (player[field] + 1) * 300
    if player["money"] < cost:
        return False, f"💸 資金不足，升級 {field} 至 Lv.{player[field]+1} 需要 ${cost}"
    player["money"] -= cost
    player[field] += 1
    update_player(player)
    return True, f"📈 {field.capitalize()} 成功升級至 Lv.{player[field]}（消耗 ${cost}）"

def update_industry_name(player_id: str, new_name: str):
    player = get_player(player_id)
    if not player:
        return False
    player["industry"] = new_name
    update_player(player)
    return True

def claim_daily(player_id):
    player = get_player(player_id)
    if not player:
        return False, "你還沒有創建企業喔！"
    now = datetime.now()
    last = player["last_daily"]
    if last:
        last_time = datetime.fromisoformat(last)
        if now.date() == last_time.date():
            return False, f"你今天已經簽到過囉！上次簽到時間：{last_time.strftime('%Y-%m-%d %H:%M:%S')}"
    player["money"] += 500
    player["last_daily"] = now.isoformat()
    update_player(player)
    return True, f"✅ 簽到成功，獲得 $500！目前資金：${player['money']}"

def upgrade_all(player_id: str):
    player = get_player(player_id)
    if not player:
        return
    player["equipment"] = 5
    player["operation"] = 5
    player["decoration"] = 5
    update_player(player)

def get_all_players():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players")
        return [dict(row) for row in cursor.fetchall()]
