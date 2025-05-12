from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from src.api.health import health_router
from src.api.post import post_router
from src.sqlite3.connection import get_session, init_db

SessionDep = Annotated[Session, Depends(get_session)]


def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, prefix="/api")
app.include_router(post_router, prefix="/api")
