import json
from pathlib import Path
from typing import Any

from fastapi import HTTPException


def settings_path() -> Path:
    return Path.home() / ".config" / "nova" / "settings.json"


def ensure_settings_file() -> Path:
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w") as file:
            json.dump({}, file, indent=2)
    elif path.stat().st_size == 0:
        with path.open("w") as file:
            json.dump({}, file, indent=2)
    return path


def load_settings_or_404() -> dict[str, Any]:
    path = settings_path()
    if not path.exists():
        raise HTTPException(status_code=404, detail="Settings not yet initialised")

    with path.open("r") as file:
        return json.load(file)
