import os
import functools

from pydantic import BaseSettings


class Config(BaseSettings):
    database_url: str
    password_secret_key: str
    token_secret_key: str
    session_secret_key: str
    algorithm: str
    access_token_expire_days: int
    file_dir: str


@functools.lru_cache()
def get_config() -> Config:
    env_path = os.environ.get("ENV_PATH")
    return Config(_env_file=env_path)