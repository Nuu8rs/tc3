from datetime import timedelta, datetime, timezone
from jose import jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Tuple, Optional

from database.models.auth import Auth
from app.components.auth.exceptions import AuthException
from app.components.auth.repo import AuthRepository
from app.components.auth.scheme import TokenData
from database.models.users import User
from app.components.users.repo import UserRepository
from app.configs import AuthConfig


class AuthService:
    def __init__(
        self, 
        auth_repository: AuthRepository, 
        user_repository: UserRepository, 
        config: AuthConfig
    ):
        self._auth_repository = auth_repository
        self._user_repository = user_repository
        self._config = config

    async def auth(self, tx: AsyncSession, token: str) -> Auth | None:
        auth = await self._auth_repository.get(tx, token)
        if auth:
            return await self._user_repository.get(tx, id=auth.user_id)
        return None

    async def create_token(
        self, tx: AsyncSession, user: User, project_id: Optional[int] = None
    ) -> Tuple[str, datetime] | Tuple[None, None]:
        expires_delta = timedelta(
            minutes=self._config.token_expiration_minutes
        )
        expires = datetime.now(timezone.utc) + expires_delta
        data = TokenData(
            user_id=user.id,
            telegram_id=user.telegram_id,
            scopes=user.scopes,
            exp=expires.timestamp(),
            current_project_id=project_id
        )
        access_token = jwt.encode(
            data.model_dump(mode="json"),
            self._config.secret_key,
            algorithm=self._config.algorithm
        )
        user = await self._user_repository.get(tx, user.id)
        user.current_project = project_id
        auth = await self._auth_repository.add(tx, user, access_token)
        if not auth:
            raise AuthException()
        return auth.token, expires
