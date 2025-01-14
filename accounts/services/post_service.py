from sqlalchemy import update, select, exists
from datetime import datetime

from typing import Optional

from accounts.session import get_session
from database.models.posts import Post
from database.models.constans import PostStatusEnum

from accounts.logger.logger import logger


class PostService:
    
    @classmethod
    async def post_exists(cls, chat_id: int, message_id: int) -> bool:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(
                        exists()
                        .where(Post.chat_id == chat_id)
                        .where(Post.message_id == message_id)
                        )
                    result = await session.execute(stmt) 
                    return bool(result.scalar())
                except Exception as E:
                    error_message = f"Error check exists post for chat_id: {chat_id} with message_id: {message_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return False
    
    @classmethod
    async def add_new_post(cls, 
                           message_id:int, 
                           chat_id: int, 
                           text: Optional[str] = None,
                           ) -> Post | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    now = datetime.utcnow().replace(tzinfo=None)

                    post_obj = Post(
                            message_id = message_id,
                            chat_id    = chat_id,
                            text       = text,
                            creation_date = now
                                   )        
                    sess.add(post_obj)
                    await sess.commit()
                    return post_obj
                
                except Exception as E:
                    error_message = f"Error creating new post for chat_id: {chat_id} with message_id: {message_id}"
                    
                    logger.error(f"{error_message}\nException: {E}")
        return None
    @classmethod
    async def edit_was_change(cls, message_id: int, chat_id: int, new_status_post: PostStatusEnum) -> None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        update(Post)
                        .where(Post.message_id  == message_id)
                        .where(Post.chat_id == chat_id)
                        .values(was_changed = new_status_post)
                    )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error edit status post for status_poost: {new_status_post} with message_id: {message_id}"
                    logger.error(f"{error_message}\nException: {E}")
                    
    @classmethod
    async def set_thumbnail_url(
        self, 
        post_id: int,
        thumbnail_url: str
    ) -> None:
        
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        update(Post)
                        .where(Post.id == post_id)
                        .values(thumbnail_url = thumbnail_url)
                    )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error edit thumbnail_url post for post_id: {post_id} with thumbnail_url: {thumbnail_url}"
                    logger.error(f"{error_message}\nException: {E}")