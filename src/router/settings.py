from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from typing import Any

from router.auth import require_api_key
from router.settings_store import (
    ensure_settings_file,
    load_settings_or_404,
)

router: APIRouter = APIRouter(prefix="/settings", tags=["settings"])


class WakeWord(BaseModel):
    id: str
    value: str


class UploadSettings(BaseModel):
    wakeWords: list[WakeWord]


def save_settings(settings: UploadSettings) -> None:
    settings_path = ensure_settings_file()
    settings_path.write_text(settings.model_dump_json(indent=2) + "\n")


@router.post("/upload", dependencies=[Depends(require_api_key)])
def upload_settings(settings: UploadSettings) -> Response:
    save_settings(settings)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/get", dependencies=[Depends(require_api_key)])
def get_settings() -> dict[str, Any]:
    return load_settings_or_404()
