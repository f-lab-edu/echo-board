from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    host: str = Field(default="127.0.0.1", alias="DEV_HOST")
    port: int = Field(default=8000, alias="DEV_PORT")

    model_config = SettingsConfigDict(env_file=".env")


dev = ServerConfig()
