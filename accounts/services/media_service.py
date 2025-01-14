from accounts.session import get_session

from database.models.posts import Media
from database.models.constans import MediaTypeEnum

from accounts.logger.logger import logger


class MediaService:

    @classmethod
    async def add_new_media(
        cls, 
        post_id: int, 
        file_url: str, 
        file_type: MediaTypeEnum, 
                            ) -> Media | None:
        async for session in get_session():
            async with session as sess:
                try:
                    new_media = Media(
                        post_id    = post_id,
                        file_url   = file_url,
                        file_type  = file_type,
                    )

                    sess.add(new_media)
                    await sess.commit()
                    return new_media
                except Exception as E:
                    error_message = f"Error adding new media {new_media}"
                    logger.error(f"{error_message}\nException: {E}")
        return None