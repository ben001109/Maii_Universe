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
