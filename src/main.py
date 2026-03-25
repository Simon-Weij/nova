import logging
from fastapi import FastAPI
from dotenv import load_dotenv

from router.settings import router as settings_router
from router.models import router as model_router
from router.auth import router as auth_router
from ai.wakeword import wakeword
from src.router.settings_store import ensure_settings_file

load_dotenv()
ensure_settings_file()

logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.error").propagate = False


app = FastAPI(root_path="/api")
app.include_router(settings_router)
app.include_router(model_router)
app.include_router(auth_router)

wakeword()


@app.get("/")
async def root():
    return {"message": "Hello World :D"}


@app.get("/health")
async def health():
    return {"status": "ok"}
