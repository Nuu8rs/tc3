from sqlalchemy import select


from bot.session import get_session
from database.models.posts import Post

from bot.logger.logger import logger


class PostService:

    @classmethod
    async def get_post(cls, post_id: int) -> Post | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (select(Post)
                            .where(Post.id == post_id)
                            ) 
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error get post = post_id: {post_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None