from fastapi import Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_babel import _ #type: ignore
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide
from starlette.templating import _TemplateResponse
from typing import Callable

from app.components.api.service import ApiService
from app.components.auth.scheme import TokenData
from app.components.auth.utils import TokenScopes, UserScopes
from app.components.chats.scheme import ChatInfoRequest, AddChatRequest, AddChatResponse
from app.components.chats.service import ChatService
from app.components.projects.service import ProjectService
from app.containers import Container, container
from database.models.users import User
from database.models.constans import ScopeEnum

chats_router = InferringRouter()


@cbv(chats_router)
class ChatsAPI:
    @inject
    def __init__(
        self,
        api_service: ApiService = Depends(Provide[Container.api_service]),
        chat_service: ChatService = Depends(Provide[Container.chat_service]),
        project_service: ProjectService = Depends(
            Provide[Container.project_service]
        ),
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._templates = templates
        self._api_service = api_service
        self._chat_service = chat_service
        self._project_service = project_service

    @chats_router.get("/sources-tg", response_model=None)
    @inject
    async def chats_list_page(
        self, 
        request: Request,
        user: User = UserScopes(ScopeEnum.CHATS_LIST),
        data: TokenData = TokenScopes(ScopeEnum.CHATS_LIST),
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> _TemplateResponse | RedirectResponse:
        async with db_session() as tx:
            chats = await self._chat_service.get_chats(tx, data)
        return self._templates.TemplateResponse(
            "chats/init.html",
            {"request": request, "_": _, "user": user, "chats": chats}
        )

    @chats_router.get("/chat-info", response_model=None)
    @inject
    async def chat_info_page(
        self, 
        request: Request,
        payload: ChatInfoRequest = Depends(),
        user: User = UserScopes(ScopeEnum.CHAT_INFO),
        data: TokenData = TokenScopes(ScopeEnum.CHAT_INFO),
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> _TemplateResponse | RedirectResponse:
        async with db_session() as tx:
            chat = await self._chat_service.get_chat(tx, payload.id, data)
            if chat is None:
                return RedirectResponse(
                    url=f"/sources-tg",
                    status_code=status.HTTP_301_MOVED_PERMANENTLY
                )
        return self._templates.TemplateResponse(
            "chat/init.html",
            {"request": request, "_": _, "user": user, "chat": chat}
        )
    
    @chats_router.post("/add-chat", response_model=AddChatResponse)
    @inject
    async def add_chat_endpoint(
        self,
        payload: AddChatRequest,
        user: User = UserScopes(ScopeEnum.CHAT_CREATE),
        data: TokenData = TokenScopes(ScopeEnum.CHAT_CREATE),
    ) -> AddChatResponse:
        response = await self._api_service.request(
            target_server="account",
            endpoint="/add-chat-to-account",
            method="POST",
            json={
                "chat_link": payload.url,
                "project_id": data.current_project_id
            }
        )
        if "message_error" in response:
            return AddChatResponse(status=response["message_error"])    
        return AddChatResponse()

container.wire(modules=[__name__])
