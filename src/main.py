import logging
from fastapi import FastAPI

from router.settings import router as settings_router

logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.error").propagate = False


app = FastAPI()
app.include_router(settings_router)


@app.get("/")
async def root():
    return {"message": "Hello World :D"}


@app.get("/health")
async def health():
    return {"status": "ok"}
