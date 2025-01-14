from sqlalchemy import insert, select

from database.models.posts import Media
from bot.session import get_session

from bot.logger.logger import logger

class MediaService:
    
    @classmethod
    async def get_media_to_post(cls, post_id: int) -> Media| list[Media] | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        select(Media)
                        .where(Media.post_id == post_id)
                    )
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error while fetching media with post_id =  {post_id}: {str(E)}"
                    logger.error(f"{error_message}")
                    