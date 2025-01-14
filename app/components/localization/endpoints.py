from dependency_injector.wiring import inject, Provide
from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from typing import Callable

from app.components.auth.utils import UserScopes
from database.models.users import User
from app.components.users.service import UserService
from app.containers import Container, container
from database.models.constans import ScopeEnum

localization_router = InferringRouter()


@cbv(localization_router)
class LocalizationAPI:
    @inject
    def __init__(
        self,
        user_service: UserService = Depends(Provide[Container.user_service]),
    ):
        self._user_service = user_service

    @localization_router.get("/set-language/{lang}/", response_model=None)
    @inject
    async def main_page(
        self, 
        lang: str, 
        request: Request,
        user: User = UserScopes(ScopeEnum.ACCOUNT_UPDATE),
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> RedirectResponse:
        async with db_session() as tx:
            user = await self._user_service.get_user(tx, user.id)
            if not user:
                return RedirectResponse(url="/")
            user.language = lang
        referer = request.headers.get("Referer", "/")
        response = RedirectResponse(url=referer)
        response.set_cookie("CurLang", lang, max_age=3600*24*365)
        return response

container.wire(modules=[__name__])
