from fastapi import Depends, HTTPException, Request
from fastapi.security import SecurityScopes
from fastapi.templating import Jinja2Templates
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide
from starlette.templating import _TemplateResponse

from app.components.auth.utils import UserScopes
from app.containers import Container, container
from database.models.constans import ScopeEnum

home_router = InferringRouter()


@cbv(home_router)
class HomeAPI:
    @inject
    def __init__(
        self,
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._templates = templates

    @home_router.get("/", name='homepage')
    @inject
    async def main_page(
        self,
        request: Request,
    ) -> _TemplateResponse:
        token = request.cookies.get('token')
        user = None
        if token:
            try:
                user = await UserScopes._validator(
                    SecurityScopes([ScopeEnum.ACCOUNT_GET.value]), token
                )
            except HTTPException:
                pass
        return self._templates.TemplateResponse(
            "home/init.html",
            {"request": request, "_": _, "user": user}
        )
    
container.wire(modules=[__name__])