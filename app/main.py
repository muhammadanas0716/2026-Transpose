from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.hx import router as hx_router
from app.routes.pages import router as pages_router


app = FastAPI(title="Homebase Hackathon Demo", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router)
app.include_router(hx_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
