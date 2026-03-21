import json
from pathlib import Path

from fastapi import HTTPException


def settings_path() -> Path:
    return Path.home() / ".config" / "nova" / "settings.json"


def ensure_settings_file() -> Path:
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    return path


def load_settings_or_404() -> dict[str, str]:
    path = settings_path()
    if not path.exists():
        raise HTTPException(status_code=404, detail="Settings not yet initialised")

    with path.open("r") as file:
        return json.load(file)
