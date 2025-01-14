from fastapi import Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide
from starlette.templating import _TemplateResponse
from typing import Callable

from app.components.auth.exceptions import TgValidationException
from app.components.auth.scheme import TokenData
from app.components.auth.service import AuthService
from app.components.auth.utils import TokenScopes, UserScopes
from app.components.projects.service import ProjectService
from app.components.projects.scheme import ChangeProjectRequest
from database.models.users import User
from app.containers import Container, container
from database.models.constans import ScopeEnum

projects_router = InferringRouter()


@cbv(projects_router)
class ProjectsAPI:
    @inject
    def __init__(
        self,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
        project_service: ProjectService = Depends(
            Provide[Container.project_service]
        ),
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._auth_service = auth_service
        self._project_service = project_service
        self._templates = templates

    @projects_router.get("/projects", response_model=None)
    @inject
    async def news_feed_page(
        self,
        request: Request,
        user: User = UserScopes(ScopeEnum.PROJECT_GET),
        data: TokenData = TokenScopes(ScopeEnum.PROJECT_GET),
        db_session: Callable = Depends(Provide[Container.db_session])
    ) -> _TemplateResponse:
        async with db_session() as tx:
            projects = await self._project_service.get_project_by_user(tx, user.id)
        return self._templates.TemplateResponse(
            "projects/init.html",
            {
                "request": request,
                "_": _,
                "user": user,
                "projects": projects,
                "token_data": data
            }
        )

    @projects_router.get("/project/switch", response_model=None)
    @inject
    async def switch_project(
        self,
        request: Request,
        response: Response,
        payload: ChangeProjectRequest = Depends(),
        user: User = UserScopes(ScopeEnum.PROJECT_GET),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> RedirectResponse:
        async with db_session() as tx:
            project = await self._project_service.get_project_by_id(tx, payload.id)
            if not project or project.user_id != user.id:
                return RedirectResponse(
                    url="/projects",
                    status_code=status.HTTP_301_MOVED_PERMANENTLY
                )
            
            token, expires = await self._auth_service.create_token(
                tx, user, payload.id
            )
            if not token:
                raise TgValidationException()

        referer = request.headers.get("Referer", "/")
        response = RedirectResponse(url=referer)
        response.set_cookie(
            key="token", value=token, expires=expires, samesite=None
        )
        return response

container.wire(modules=[__name__])
