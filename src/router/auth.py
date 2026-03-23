import bcrypt
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status

from router.settings_store import load_password_hash_or_404

import hashlib

verified_key_cache: set[str] = set()
router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing password")

    cache_key = hashlib.sha256(x_api_key.encode()).hexdigest()
    if cache_key in verified_key_cache:
        return

    hashed_password = load_password_hash_or_404()

    is_valid = bcrypt.checkpw(x_api_key.encode(), hashed_password.encode())
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid password")

    verified_key_cache.add(cache_key)


@router.get("/check", dependencies=[Depends(require_api_key)])
def check_auth() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
