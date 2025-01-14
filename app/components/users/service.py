import hmac
import hashlib
import urllib.parse

from sqlmodel.ext.asyncio.session import AsyncSession

from app.components.auth.exceptions import TgValidationException, PasswordException
from app.components.users.repo import UserRepository
from app.configs import AuthConfig
from database.models.users import User


class UserService:
    def __init__(self, user_repository: UserRepository, config: AuthConfig):
        self._user_repository = user_repository
        self._config = config

    async def get_user(self, tx: AsyncSession, user_id: int) -> User | None:
        return await self._user_repository.get(tx, id=user_id)
    
    async def auth_user(self, tx: AsyncSession, user_data: dict) -> User:
        user = await self._user_repository.get(
            tx, 
            login=user_data.get("username", None), 
            telegram_id=user_data.get("id")
        )
        if user:
            if user_data.get("password", "") != user.hashed_password: # TODO hashed password
                raise PasswordException()
            login = user_data.get("username", None)
            if isinstance(login, str) and login != user.login:
                user.login = login
        else:
            user = await self._user_repository.add(tx, user_data)
        if not user:
            raise PasswordException()
        return user

    @staticmethod
    def str_to_dict(raw_str: str) -> dict:
        return {
            k: urllib.parse.unquote(v) for k, v in [
                s.split('=', 1) for s in raw_str.split('&')
            ]
        }

    def get_tg_auth_hash(self, data: dict) -> str:
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash'
        )
        secret_key = hmac.new(
            "WebAppData".encode(), 
            self._config.bot_token.encode(),
            hashlib.sha256
        ).digest()
        h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
        return h.hexdigest()
    
    def validate_tg_data(self, data_str: str) -> dict | None:
        data = self.str_to_dict(data_str)
        hash = self.get_tg_auth_hash(data)
        if hash != data.get("hash", None):
            raise TgValidationException()
        return data
