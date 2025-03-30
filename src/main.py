from fastapi import FastAPI

from src.api.health import health_router
from src.api.post import post_router

app = FastAPI()
app.include_router(health_router, prefix="/api")
app.include_router(post_router, prefix="/api")
