import json
from pathlib import Path
from typing import Any

from fastapi import HTTPException


def settings_path() -> Path:
    return Path.home() / ".config" / "nova" / "settings.json"


def password_path() -> Path:
    return Path.home() / ".config" / "nova" / "password.txt"


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


def ensure_password_file() -> Path:
    path = password_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    return path


def load_settings_or_404() -> dict[str, Any]:
    path = settings_path()
    if not path.exists():
        raise HTTPException(status_code=404, detail="Settings not yet initialised")

    with path.open("r") as file:
        return json.load(file)


def load_password_hash_or_404() -> str:
    path = password_path()
    if not path.exists():
        raise HTTPException(status_code=404, detail="Password not set")

    hashed_password = path.read_text().strip()
    if not hashed_password:
        raise HTTPException(status_code=404, detail="Password not set")

    return hashed_password
