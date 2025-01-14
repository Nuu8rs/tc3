from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Sequence, Optional, Tuple

from database.models.posts import Post
from app.components.auth.scheme import TokenData
from app.components.chats.service import ChatService
from app.components.posts.exceptions import PostNotFoundException
from app.components.posts.repo import PostRepository


class PostService:
    def __init__(
        self,
        post_repository: PostRepository,
        chat_service: ChatService,
    ):
        self._chat_service = chat_service
        self._post_repository = post_repository

    async def add_post(self, tx: AsyncSession,post: Post) -> Post | None:
        return await self._post_repository.add_post(tx, post)    

    async def get_posts(
        self,
        tx: AsyncSession,
        data: TokenData,
        page: int
    ) -> Tuple[Sequence[Post], int]:
        chats = await self._chat_service.get_chats(tx, data)
        if not chats:
            return (), 0
        chats_id = [c.chat_id for c in chats]
        posts = await self._post_repository.get_posts(tx, chats_id, page)
        total_posts = await self._post_repository.get_posts_count(
            tx, chats_id
        )
        return posts, total_posts

    async def get_post(
        self,
        tx: AsyncSession, 
        post_id: int,
        data: TokenData
    ) -> Post:
        chats = await self._chat_service.get_chats(tx, data)
        if not chats:
            raise PostNotFoundException()
        chats_id = [c.chat_id for c in chats]
        post = await self._post_repository.get_post(tx, chats_id, post_id)
        if not post:
            raise PostNotFoundException()
        return post
    
    async def get_custom_post(
        self,
        tx: AsyncSession,
        post: Post,
        project_id: int,
        new_thumbnail: Optional[str] = None, # TODO make working with video
        new_text: Optional[str] = None
    ) -> Post | None:
        if post.project_id is None:
            new_post = Post(
                chat_id=post.chat_id,
                message_id=post.message_id,
                text=post.text if new_text is None else new_text,
                creation_date=post.creation_date,
                project_id=project_id,
                was_changed=post.was_changed,
                thumbnail_url=new_thumbnail or post.thumbnail_url
            )
            return await self.add_post(tx, new_post)
        elif new_thumbnail is not None:
            post.thumbnail_url = new_thumbnail
        elif new_text is not None:
            post.text = new_text
        return post
