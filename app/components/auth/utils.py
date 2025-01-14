from aiocache import cached #type: ignore
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.params import Security
from fastapi.security import OAuth2, SecurityScopes
from jose import jwt, JWTError
from typing import Any, Callable, Dict, Optional, Sequence, cast, Tuple

from app.configs import AuthConfig
from app.containers import Container, container
from app.components.auth.exceptions import (
    AuthException,
    InvalidTokenDataException,
    NoTokenException,
    PermissionsException,
    TokenDecodeException,
)
from app.components.auth.scheme import TokenData
from app.components.users.repo import UserRepository
from database.models.constans import ScopeEnum
from database.models.users import User


class OAuth2CookieJWT(OAuth2):
    """
    OAuth2 flow for authentication using a cookie token.
    An instance of it would be used as a dependency.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get("token", None)
        if not token:
            if self.auto_error:
                raise AuthException()
            else:
                return None
        return token

oauth2_scheme = OAuth2CookieJWT(
    tokenUrl="auth/tg",
    scopes={
        ScopeEnum.ACCOUNT_GET: "Get my account info",
        ScopeEnum.ACCOUNT_UPDATE: "Update my account info",
        ScopeEnum.ACCOUNT_DELETE: "Delete my account",

        ScopeEnum.ACCOUNTS_GET: "Get info of any account",
        ScopeEnum.ACCOUNTS_CREATE: "Create new account",
        ScopeEnum.ACCOUNTS_UPDATE: "Update info of any account",
        ScopeEnum.ACCOUNTS_DELETE: "Delete any account",

        ScopeEnum.PROJECT_GET: "Get list of projects by owner",
        ScopeEnum.PROJECT_CREATE: "Creata new project",
        ScopeEnum.PROJECT_DELETE: "Delete my project",

        ScopeEnum.CHATS_LIST: "Get list of chats by project",
        # ScopeEnum.MODERATORS_LIST: "Get list of moderators by project",
        ScopeEnum.POSTS_LIST: "Get list of posts by project",

    },
    auto_error=False
)


class BaseScopes(Security):
    _validator: Callable

    def __init__(
        self,
        scopes: str | Sequence[str],
        *,
        use_cache: bool = True,
    ):
        scopes = [scopes] if isinstance(scopes, str) else scopes
        super().__init__(
            dependency=self._validator,
            scopes=scopes,
            use_cache=use_cache
        )

    @staticmethod
    def check_scopes(token_scopes: str, required_scopes: str):
        if token_scopes == "*:*":
            return True
        
        rscopes = required_scopes.split(" ")
        if not rscopes:
            return True
        
        for scope in token_scopes.split(" "):
            group, func = scope.split(":")
            cur_rscope_i = 0

            while cur_rscope_i < len(rscopes):
                rgroup, rfunc = rscopes[cur_rscope_i].split(":")
                if group in ("*", rgroup) and func in ("*", rfunc):
                    del rscopes[cur_rscope_i]
                else:
                    cur_rscope_i += 1

        return not rscopes


class TokenScopes(BaseScopes):
    @classmethod
    @inject
    async def _validator(
        cls,
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        config: AuthConfig = Depends(Provide[Container.config.provided.auth]),
    ) -> TokenData:
        if not token:
            raise NoTokenException()
        try:
            payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        except JWTError as e:
            raise TokenDecodeException()
        data = TokenData(**payload)
        if data.user_id is None:
            raise InvalidTokenDataException()
        if data.scopes is None:
            raise InvalidTokenDataException()
        is_enough = cls.check_scopes(data.scopes, " ".join(security_scopes.scopes))
        if not is_enough:
            raise PermissionsException()
        return data


class UserScopes(TokenScopes):
    @classmethod
    @inject
    async def _validator(
        cls,
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
    ) -> Tuple[User, TokenData]:
        data = await super()._validator(security_scopes, token)
        user = await cls._get_account_cached(data.user_id)
        if user is None:
            raise AuthException()
        return user

    @staticmethod
    @cached(ttl=60 * 5)  # 5 minutes ttl
    @inject
    async def _get_account_cached(
        user_id: int,
        db_session: Callable = Depends(Provide[Container.db_session]),
        user_repo: UserRepository = Depends(Provide[Container.user_repository]),
    ) -> User | None:
        async with db_session() as tx:
            return await user_repo.get(tx, id=user_id)

container.wire(modules=[__name__])
