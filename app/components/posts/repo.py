from sqlalchemy import and_, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from database.models.posts import Post
from app.constants import PAGINATION_SIZE


class PostRepository:
    @staticmethod
    async def add_post(
        tx: AsyncSession, 
        post: Post
    ) -> Post | None:
        try:
            tx.add(post)
            await tx.flush()
            await tx.refresh(post)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            await tx.rollback()
            return None
        return post
    
    @staticmethod
    async def get_posts(
        tx: AsyncSession,
        chats_id: list[int], page: int
    ) -> Sequence[Post]:
        q = select(Post).where(
            Post.chat_id.in_(chats_id)
        ).order_by(
            desc(Post.creation_date)
        ).limit(PAGINATION_SIZE).offset(page*PAGINATION_SIZE)
        result = await tx.execute(q)
        return result.scalars().all()

    @staticmethod
    async def get_posts_count(
        tx: AsyncSession,
        chats_id: list[int]
    ) -> int:
        q = select(func.count(Post.id)).where(
            Post.chat_id.in_(chats_id)
        )
        result = await tx.execute(q)
        return result.scalar()

    @staticmethod
    async def get_post(
        tx: AsyncSession,
        chats_id: list[int],
        post_id: int
    ) -> Post | None:
        q = select(Post).where(
            and_(
                Post.id == post_id,
                Post.chat_id.in_(chats_id)
            )
        )
        result = await tx.execute(q)
        return result.scalar_one_or_none()
