import math

from fastapi import Depends, Request, Path
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
from app.components.media.service import MediaService
from app.components.posts.exceptions import PostNotFoundException
from app.components.posts.service import PostService
from app.components.posts.scheme import (
    PostInfoRequest,
    SendPostRequest,
    UpdatePostRequest,
    SendPostResponse,
    UpdatePostResponse
)
from app.constants import PAGINATION_SIZE
from app.containers import Container, container
from database.models.constans import ScopeEnum
from database.models.users import User

posts_router = InferringRouter()


@cbv(posts_router)
class PostsAPI:
    @inject
    def __init__(
        self,
        api_service: ApiService = Depends(Provide[Container.api_service]),
        media_service: MediaService = Depends(Provide[Container.media_service]),
        post_service: PostService = Depends(Provide[Container.post_service]),
        templates: Jinja2Templates = Depends(Provide[Container.templates]),
    ):
        self._templates = templates
        self._api_service = api_service
        self._media_service = media_service
        self._post_service = post_service

    @posts_router.get("/news", name='news', response_model=None)
    @inject
    async def news_first_page(
        self, 
        request: Request,
        page: int = 0,
        user: User = UserScopes(ScopeEnum.POSTS_LIST),
        data: TokenData = TokenScopes(ScopeEnum.POSTS_LIST),
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> _TemplateResponse:
        if data.current_project_id:
            async with db_session() as tx:
                posts, count = await self._post_service.get_posts(tx, data, page)
        else:
            posts = ()
            count = 0
        if page > 0 and len(posts) == 0:
            return RedirectResponse(url="/news")
        
        max_page = math.ceil(count / PAGINATION_SIZE)
        return self._templates.TemplateResponse(
            "posts/init.html",
            {
                "request": request,
                "_": _,
                "user": user,
                "posts": posts,
                "max_page": max_page,
                "page": page
            }
        )

    @posts_router.get("/news/{page}", response_model=None)
    async def news_pages(
        self, 
        request: Request,
        page: int = Path(title="Current page."),
        user: User = UserScopes(ScopeEnum.POSTS_LIST),
        data: TokenData = TokenScopes(ScopeEnum.POSTS_LIST),
        db_session: Callable = Depends(Provide[Container.db_session]), 
    ) -> _TemplateResponse:
        return await self.news_first_page(
            request,
            page=page,
            user=user,
            data=data,
            db_session=db_session
        )
    
    @posts_router.get("/post-info", response_model=None)
    @inject
    async def post_info(
        self,
        request: Request,
        payload: PostInfoRequest = Depends(),
        user: User = UserScopes(ScopeEnum.POST_INFO),
        data: TokenData = TokenScopes(ScopeEnum.POST_INFO),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> _TemplateResponse | RedirectResponse:
        async with db_session() as tx:
            try:
                post = await self._post_service.get_post(tx, payload.post_id, data)
            except PostNotFoundException:
                return RedirectResponse(
                    url=request.headers.get("Referer", "/news")
                )
            else:
                medias = await self._media_service.get_media_by_post_id(tx, post.id)
        return self._templates.TemplateResponse(
            "post/init.html",
            {
                "request": request,
                "_": _,
                "user": user,
                "post": post,
                "medias": medias
            }
        )

    @posts_router.post("/update-post", response_model=UpdatePostResponse)
    @inject
    async def update_post(
        self,
        payload: UpdatePostRequest,
        user: User = UserScopes(ScopeEnum.POST_UPDATE),
        data: TokenData = TokenScopes(ScopeEnum.POST_UPDATE),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> UpdatePostResponse:
        async with db_session() as tx:
            post = await self._post_service.get_post(
                tx, payload.post_id, data
            )
            new_post = await self._post_service.get_custom_post(
                tx, post, data.current_project_id, new_text=payload.text
            )

            if post.id != new_post.id:
                await self._media_service.copy_media(tx, post, new_post)
        return UpdatePostResponse(post_id=new_post.id)

    @posts_router.post("/send-post", response_model=SendPostResponse)
    @inject
    async def send_post(
        self,
        payload: SendPostRequest,
        user: User = UserScopes(ScopeEnum.POST_INFO),
        data: TokenData = TokenScopes(ScopeEnum.POST_INFO),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> SendPostResponse:
        if payload.text:
            response = await self.update_post(payload, user, data)
            payload.post_id = response.post_id
        async with db_session() as tx:
            post = await self._post_service.get_post(tx, payload.post_id, data)

            await self._api_service.request(
                target_server="bot",
                endpoint="/sendPost",
                method="POST",
                json={
                    "post_id": post.id,
                    "project_id": data.current_project_id
                }
            )
        return SendPostResponse(post_id=payload.post_id)

container.wire(modules=[__name__])
