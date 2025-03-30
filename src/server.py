import uvicorn

from src import config


def run():
    uvicorn.run(
        "src.main:app", host=config.dev.host, port=config.dev.port, reload=True
    )
