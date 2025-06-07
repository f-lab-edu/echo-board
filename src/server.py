import uvicorn

from src.config import dev

# COMMENT: 보통 이 로직은 main.py 내 __main__ 안에 두곤 합니다.
def run():
    uvicorn.run("src.main:app", host=dev.host, port=dev.port, reload=True)
