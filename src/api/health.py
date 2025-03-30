from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health")
async def _health_ckeck() -> dict[str, str]:
    return {
        "status": "ok",
    }
