from sqlalchemy import select

from accounts.session import get_session
from database.models.proxy import Proxy

from accounts.logger.logger import logger

class ProxyService:
    
    @classmethod
    async def get_proxy(cls, proxy_id: int) -> Proxy:
        async for session in get_session():
            async with session as sess: 
                try:
                    result = await sess.execute(
                        select(Proxy).where(Proxy.id == proxy_id)
                    )
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error fetching proxy with proxy_id: {proxy_id}"
                    logger.error(f"{error_message}\nException: {E}")


        