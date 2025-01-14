import json

from typing import Callable
from dependency_injector.wiring import inject, Provide
from fastapi import Depends, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.templating import _TemplateResponse

from app.components.users.service import UserService
from app.components.auth.scheme import ValidateTelegramData, AuthTGModel
from app.components.auth.service import AuthService
from app.containers import Container, container

auth_router = InferringRouter()


@cbv(auth_router)
class AuthAPI:
    @inject
    def __init__(
        self,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
        user_service: UserService = Depends(Provide[Container.user_service]),
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._templates = templates
        self._auth_service = auth_service
        self._user_service = user_service

    @auth_router.get(
        "/auth",
        response_model=None
    )
    @inject
    async def auth(
        self,
        request: Request
    ) -> _TemplateResponse:
        return self._templates.TemplateResponse(
            "auth/init.html",
            {"request": request, "_": _}
        )


    @auth_router.post(
        "/auth/tg",
        response_model=ValidateTelegramData
    )
    @inject
    async def auth_tg(
        self,
        response: Response,
        raw_data: AuthTGModel,
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> ValidateTelegramData:
        data = self._user_service.validate_tg_data(raw_data.data)

        async with db_session() as tx:
            user = await self._user_service.auth_user(
                tx, json.loads(data["user"])
            )
            token, expires = await self._auth_service.create_token(
                tx, user, user.current_project
            )

        response.set_cookie(
            key="token", value=token, expires=expires, samesite=None
        )
        return ValidateTelegramData(valid=True)

container.wire(modules=[__name__])
