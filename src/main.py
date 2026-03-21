from fastapi import FastAPI

from router.settings import router as settings_router

app = FastAPI()
app.include_router(settings_router)


@app.get("/")
async def root():
    return {"message": "Hello World :D"}
