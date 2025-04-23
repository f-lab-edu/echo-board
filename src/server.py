import uvicorn

from src.config import dev


def run():
    uvicorn.run("src.main:app", host=dev.host, port=dev.port, reload=True)
