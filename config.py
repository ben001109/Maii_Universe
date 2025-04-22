import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _config = json.load(f)

TOKEN = _config.get("token")
ADMIN_IDS = _config.get("admin_ids", [])