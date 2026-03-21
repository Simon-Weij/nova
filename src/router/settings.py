import json
import logging
import os
from fastapi import APIRouter, HTTPException
from pathlib import Path
from pydantic import BaseModel
import bcrypt


router = APIRouter(prefix="/settings", tags=["settings"])


class Settings(BaseModel):
    password: str


@router.post("/upload")
def upload_settings(settings: Settings):
    homedir: str = os.environ["HOME"]
    path: Path = Path(homedir + ".config/nova/settings.json")

    if not path.exists():
        path.touch()

    hashed_password: bytes = bcrypt.hashpw(settings.password.encode(), bcrypt.gensalt())

    with open(path, "w") as f:
        json.dump({"password": hashed_password.decode()}, f, indent=2)


@router.get("/get")
def get_settings():
    homedir: str = os.environ["HOME"]
    path: Path = Path(homedir + ".config/nova/settings.json")

    if not path.exists():
        logging.info("Settings file was not found.")
        raise HTTPException(status_code=404, detail="Settings not yet initialised")
    else:
        with path.open() as f:
            return json.load(f)
