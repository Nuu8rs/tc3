from datetime import datetime
from sqlalchemy import update

from accounts.constans import NO_VIEWS
from accounts.session import get_session
from accounts.logger.logger import logger

from database.models.posts import Views


class ViewService:
    
    @classmethod
    async def add_new_views(
        cls, 
        chat_id: int,
        message_id: int,
    ) -> Views | None:
    
        async for session in get_session():
            async with session as sess: 
                try:      
                    now = datetime.utcnow().replace(tzinfo=None)
                              
                    new_views = Views(
                        chat_id = chat_id,
                        message_id = message_id,
                        views  = NO_VIEWS,
                        tracking_time = now
                    )
                    sess.add(new_views)
                    await sess.commit()
                    return new_views
                except Exception as E:
                    error_message = f"Error create new views with chat_id: {chat_id} | message_id: {message_id} | "
                    logger.error(f"{error_message}\nException: {E}")
        return None
                
    @classmethod
    async def update_amount_views(cls, id_views: int, amount_views: int) -> None:
        async for session in get_session():
            async with session as sess: 
                try:   
                    stmt = (
                        update(Views)
                        .where(Views.id == id_views)
                        .values(views = amount_views)
                        )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error update  views with id_views: {id_views}"
                    logger.error(f"{error_message}\nException: {E}")
                    