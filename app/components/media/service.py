from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional

from app.components.media.repo import MediaRepository
from database.models.posts import Media, Post


class MediaService:
    def __init__(
        self,
        media_repository: MediaRepository,
    ):
        self._media_repository = media_repository

    async def add_media(self, tx: AsyncSession, media: Media) -> Media:
        return await self._media_repository.add_media(tx, media)

    async def copy_media(
        self,
        tx: AsyncSession,
        old_post: Post,
        new_post: Post
    ) -> None:
        media_files = await self.get_media_by_post_id(tx, old_post.id)
        for media in media_files:
            new_media = Media(
                post_id = new_post.id,
                file_url=media.file_url,
                file_type=media.file_type
            )
            await self.add_media(tx, new_media)

    async def get_media(
        self,
        tx: AsyncSession,
        post_id: int,
        url: Optional[str] = None
    ) -> Media | None:
        return await self._media_repository.get_media(
            tx, post_id, url
        )
    
    async def get_new_thumbnail(
        self,
        tx: AsyncSession,
        post_id: int,
        old_thumbnail_url: str
    ) -> Media | None:
        return await self._media_repository.get_media(
            tx, post_id, old_thumbnail_url=old_thumbnail_url
        )

    async def get_media_by_post_id(
        self, 
        tx: AsyncSession, 
        post_id: int
    ) -> List[Media]:
        return await self._media_repository.get_media_by_post_id(
            tx, post_id=post_id
        )
    
    async def delete_media(self, tx: AsyncSession, media: Media) -> None:
        await self._media_repository.delete_media(tx, media)
