from database import get_player, update_player

def required_exp(level: int) -> int:
    return 100 + (level - 1) * 100

def gain_exp(player_id: str, amount: int) -> bool:
    player = get_player(player_id)
    if not player:
        return False
    player["exp"] += amount
    leveled_up = False
    while player["exp"] >= required_exp(player["level"]):
        player["exp"] -= required_exp(player["level"])
        player["level"] += 1
        leveled_up = True
    update_player(player)
    return leveled_up

def simulate_hourly_income(player_id: str) -> float:
    player = get_player(player_id)
    if not player:
        return 0.0
    base_income = 10
    income = base_income + player["equipment"] * 5 + player["operation"] * 3 + player["decoration"] * 2 + player["level"] * 1.5
    player["money"] += income
    player["exp"] += 10
    leveled_up = False
    while player["exp"] >= required_exp(player["level"]):
        player["exp"] -= required_exp(player["level"])
        player["level"] += 1
        leveled_up = True
    update_player(player)
    return income

def get_default_player(player_id: str, name: str) -> dict:
    return {
        "id": player_id,
        "name": name,
        "money": 500.0,
        "exp": 0,
        "level": 1,
        "equipment": 0,
        "operation": 0,
        "decoration": 0,
        "industry": "未命名企業",
        "last_daily": None,
        "last_work": None
    }
