from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request

from app.api.router import main_router
from app.core.config import settings
from app.core.init_db import start_db_script
from app.services.telegram import start_telegram, stop_telegram, send_message

ENV_FILE = Path().resolve().parent / ".env"
app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(main_router)


@app.middleware("http")
async def send_exceptions_to_telegram(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        await send_message(str(e))
        raise e


@app.on_event("startup")
async def startup():
    await start_db_script()
    await start_telegram()


@app.on_event("shutdown")
async def shutdown():
    await stop_telegram()


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=settings.service_port, reload=True, env_file=ENV_FILE
    )
