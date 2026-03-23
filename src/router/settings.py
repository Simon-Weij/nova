from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
import bcrypt
from typing import Any

from router.auth import require_api_key, verified_key_cache
from router.settings_store import (
    ensure_password_file,
    ensure_settings_file,
    load_password_hash_or_404,
    load_settings_or_404,
)

router: APIRouter = APIRouter(prefix="/settings", tags=["settings"])



class Settings(BaseModel):
    password: str


class WakeWord(BaseModel):
    id: str
    value: str


class UploadSettings(BaseModel):
    wakeWords: list[WakeWord]


@router.get("/status")
def get_settings_status() -> Response:
    load_password_hash_or_404()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def save_password(settings: Settings) -> None:
    verified_key_cache.clear()
    password_file_path = ensure_password_file()
    settings_path = ensure_settings_file()
    hashed_password: bytes = bcrypt.hashpw(settings.password.encode(), bcrypt.gensalt())

    password_file_path.write_text(hashed_password.decode())
    settings_path.write_text("{}\n")


def save_settings(settings: UploadSettings) -> None:
    settings_path = ensure_settings_file()
    settings_path.write_text(settings.model_dump_json(indent=2) + "\n")


@router.post("/upload-password")
def upload_password(settings: Settings) -> Response:
    save_password(settings)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/upload", dependencies=[Depends(require_api_key)])
def upload_settings(settings: UploadSettings) -> Response:
    save_settings(settings)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/get", dependencies=[Depends(require_api_key)])
def get_settings() -> dict[str, Any]:
    settings_data = load_settings_or_404()
    settings_data.pop("password", None)
    return settings_data
