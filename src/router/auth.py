import os
import secrets
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status


PASSWORD_ENV_VAR = "NOVA_PASSWORD"
router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


def get_configured_password_or_500() -> str:
    configured_password = os.getenv(PASSWORD_ENV_VAR, "").strip()
    if not configured_password:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required environment variable: {PASSWORD_ENV_VAR}",
        )

    return configured_password


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing password")

    configured_password = get_configured_password_or_500()
    is_valid = secrets.compare_digest(x_api_key, configured_password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid password")


@router.get("/check", dependencies=[Depends(require_api_key)])
def check_auth() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
