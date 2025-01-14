from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide
from starlette.templating import _TemplateResponse

from app.components.auth.utils import UserScopes
from database.models.users import User
from app.containers import Container, container
from database.models.constans import ScopeEnum

user_router = InferringRouter()


@cbv(user_router)
class ProfileAPI:
    @inject
    def __init__(
        self,
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._templates = templates

    @user_router.get("/profile", name='profile', response_model=None)
    @inject
    async def profile_page(
        self, 
        request: Request,
        user: User = UserScopes(ScopeEnum.ACCOUNT_GET),
    ) -> _TemplateResponse:
        return self._templates.TemplateResponse(
            "profile/init.html",
            {"request": request, "_": _, "user": user}
        )

container.wire(modules=[__name__])
