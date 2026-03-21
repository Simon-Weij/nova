import json
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
import bcrypt

from router.auth import require_api_key, verified_key_cache
from router.settings_store import ensure_settings_file, load_settings_or_404


router = APIRouter(prefix="/settings", tags=["settings"])


class Settings(BaseModel):
    password: str


@router.get("/status")
def get_settings_status() -> Response:
    data = load_settings_or_404()
    if not data.get("password"):
        raise HTTPException(status_code=404, detail="Password not set")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/upload")
def upload_settings(settings: Settings) -> Response:
    verified_key_cache.clear()
    path = ensure_settings_file()
    hashed_password: bytes = bcrypt.hashpw(settings.password.encode(), bcrypt.gensalt())

    with path.open("w") as file:
        json.dump({"password": hashed_password.decode()}, file, indent=2)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/get", dependencies=[Depends(require_api_key)])
def get_settings() -> dict[str, str]:
    settings_data = load_settings_or_404()
    settings_data.pop("password", None)
    return settings_data
