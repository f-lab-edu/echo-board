from fastapi import FastAPI

from src.api.health import health_router

app = FastAPI()
app.include_router(health_router, prefix="/api")
