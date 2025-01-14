from pydantic import BaseModel
from typing import Set, List

class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    token_expiration_minutes: float
    bot_token: str


class DbConfig(BaseModel):
    master: str
    master_sync: str
    master_pool_min_size: int
    master_pool_max_size: int


class EnvConfig(BaseModel):
    port: int
    enable_cors: bool
    debug: bool
    base_api_url: str
    base_bot_api_url: str


class MediaConfig(BaseModel):
    media_dir: List[str]
    media_endpoint: str
    max_file_size_mb: int
    allowed_file_types: Set[str]


class AppConfig(BaseModel):
    env: EnvConfig
    db: DbConfig
    auth: AuthConfig
    media: MediaConfig
