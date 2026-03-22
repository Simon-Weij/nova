import os
from fastapi import APIRouter, Depends, HTTPException
import ollama
from pydantic import BaseModel
from src.router.auth import require_api_key


router: APIRouter = APIRouter(prefix="/models", tags=["models"])

OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")


class PullModelRequest(BaseModel):
    model_name: str


@router.get(path="/", dependencies=[Depends(dependency=require_api_key)])
async def get_installed_models() -> list[dict[str, str]]:
    client = ollama.Client(host=OLLAMA_HOST)
    response = client.list()
    return [
        {
            "name": model.model or "unknown",
            "size": f"{(model.size or 0) / 1e9:.1f} GB",
        }
        for model in response.models
    ]


@router.post("/", dependencies=[Depends(require_api_key)])
def install_new_model(request: PullModelRequest):
    requested_name = request.model_name.strip()
    if not requested_name:
        raise HTTPException(status_code=400, detail="model_name is required")

    client = ollama.Client(host=OLLAMA_HOST)

    installed_names = {model.model for model in client.list().models if model.model}
    if requested_name in installed_names:
        return {"status": "already-installed", "model": requested_name}

    try:
        client.pull(requested_name, stream=False)
        return {"status": "installed", "model": requested_name}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{model_name:path}", dependencies=[Depends(require_api_key)])
async def delete_model(model_name: str):
    requested_name = model_name.strip()
    if not requested_name:
        raise HTTPException(status_code=400, detail="model_name is required")

    client = ollama.Client(host=OLLAMA_HOST)

    try:
        client.delete(requested_name)
        return {"status": "deleted", "model": requested_name}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error