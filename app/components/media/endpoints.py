import aiofiles
import asyncio # import aiofiles.os as aio_os

from fastapi import Depends, UploadFile, File, Form, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide
from pathlib import Path
from random import random
from typing import Callable, List

from app.components.auth.scheme import TokenData
from app.components.auth.utils import TokenScopes, UserScopes
from app.components.media.exceptions import (
    AddMediaException,
    DeleteMediaException
)
from app.components.media.scheme import (
    DeleteFileRequest,
    DeleteFileResponse,
    UploadFileResponse
)
from app.components.media.service import MediaService
from app.components.posts.utils import validate_media
from app.components.posts.service import PostService
from app.constants import DEFAULT_THUMBNAIL
from app.containers import Container, container
from database.models.constans import ScopeEnum, MediaTypeEnum
from database.models.posts import Media
from database.models.users import User

media_router = InferringRouter()


@cbv(media_router)
class MediaAPI:
    @inject
    def __init__(
        self,
        post_service: PostService = Depends(Provide[Container.post_service]),
        media_service: MediaService = Depends(Provide[Container.media_service]),
    ):
        self._media_service = media_service
        self._post_service = post_service

    @media_router.post(
        "/upload-file",
        response_model=UploadFileResponse,
        status_code=status.HTTP_201_CREATED
    )
    @inject
    async def upload_media(
        self,
        post_id: int = Form(..., description="Unique ID of the post"),
        files: List[UploadFile] = File(...),
        user: User = UserScopes(ScopeEnum.POST_UPDATE),
        data: TokenData = TokenScopes(ScopeEnum.POST_UPDATE),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> UploadFileResponse:
        media_urls = []

        async with db_session() as tx:
            post = await self._post_service.get_post(tx, post_id, data)
            if not post:
                raise AddMediaException()
            for file in files:
                file_path, file_url = validate_media(file)

                is_image = "image" in file.content_type
                new_post = await self._post_service.get_custom_post(
                    tx,
                    post,
                    data.current_project_id,
                    file_url if is_image else None
                )
                if post.id != new_post.id:
                    await self._media_service.copy_media(tx, post, new_post)

                media = Media(
                    post_id=new_post.id,
                    file_url=file_url,
                    file_type=(
                        MediaTypeEnum.PHOTO 
                        if is_image else 
                        MediaTypeEnum.VIDEO
                    )
                )
                media = await self._media_service.add_media(tx, media)
                media_urls.append(media.file_url)
                post = new_post

                async with aiofiles.open(file_path, "wb") as f:
                    while content := await file.read(1024 * 1024):
                        await f.write(content)
        return UploadFileResponse(urls=media_urls, post_id=new_post.id)

    @media_router.post(
        "/delete-file",
        response_model=DeleteFileResponse,
        status_code=status.HTTP_200_OK
    )
    @inject
    async def delete_media(
        self,
        payload: DeleteFileRequest,
        user: User = UserScopes(ScopeEnum.POST_UPDATE),
        data: TokenData = TokenScopes(ScopeEnum.POST_UPDATE),
        db_session: Callable = Depends(Provide[Container.db_session]),
    ) -> DeleteFileResponse:
        file_path = Path("accounts"+payload.url)
        if not file_path.exists() or not file_path.is_file():
            raise DeleteMediaException()
        
        async with db_session() as tx:
            media = await self._media_service.get_media(
                tx, payload.post_id, payload.url
            )

            post = await self._post_service.get_post(tx, media.post_id, data)
            if not post:
                raise DeleteMediaException()

            new_thumbnail = await self._media_service.get_new_thumbnail(
                tx, post.id, media.file_url
            )
            if new_thumbnail is None:
                new_thumbnail_url = DEFAULT_THUMBNAIL
            else:
                new_thumbnail_url = new_thumbnail.file_url

            new_post = await self._post_service.get_custom_post(
                tx, post, data.current_project_id, new_thumbnail_url
            )

            if post.id != new_post.id:
                await self._media_service.copy_media(tx, post, new_post)
                media_to_delete = await self._media_service.get_media(
                    tx, new_post.id, media.file_url
                )
            else:
                media_to_delete = media

            await self._media_service.delete_media(
                tx, media_to_delete
            )
        return DeleteFileResponse(post_id=new_post.id)

container.wire(modules=[__name__])
