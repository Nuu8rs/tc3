from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional

from app.components.base.exceptions import LogicError
from database.models.constans import MediaTypeEnum
from database.models.posts import Media


class MediaRepository:
    @staticmethod
    async def add_media(tx: AsyncSession, media: Media) -> Media:
        tx.add(media)
        try:
            await tx.flush()
        except IntegrityError:
            raise LogicError("Invalid media data")
        await tx.commit()
        await tx.refresh(media)
        return media
    
    @staticmethod
    async def get_media(
        tx: AsyncSession,
        post_id: int,
        url: Optional[str] = None,
        old_thumbnail_url: Optional[str] = None
    ) -> Media | None:
        q = select(Media).where(Media.post_id == post_id)

        if url is not None:
            q = q.where(
                Media.file_url == url
            )

        if old_thumbnail_url is not None:
            q = q.where(
                and_(
                    Media.file_url != old_thumbnail_url,
                    Media.file_type == MediaTypeEnum.PHOTO
                )
            )
        q = q.limit(1)
        result = await tx.execute(q)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_media_by_post_id(
        tx: AsyncSession,
        post_id: int
    ) -> Sequence[Media]:
        q = select(Media).where(
            Media.post_id == post_id
        )
        result = await tx.execute(q)
        return result.scalars().all()

    @staticmethod
    async def delete_media(tx: AsyncSession, media: Media) -> None:
        await tx.delete(media)
        await tx.flush()