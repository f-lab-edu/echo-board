from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# DONE: 파이썬에서 설정 파일을 다루는 여러 방식들에 대해 설명하기 ✅
# ❕(과제. 각 방법에 대해서 예시로 구현해보기) ✅
class ServerConfig(BaseSettings):
    host: str = Field(default="127.0.0.1", alias="DEV_HOST")
    port: int = Field(default=8000, alias="DEV_PORT")

    model_config = SettingsConfigDict(env_file=".env")


dev = ServerConfig()
