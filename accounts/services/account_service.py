from accounts.session import get_session
from database.models.account_info import AccountInfo

from sqlalchemy.future import select

from accounts.logger.logger import logger

class AccountService:

    @classmethod
    async def get_all_accounts(cls) -> AccountInfo | None:
        async for session in get_session():
            async with session as sess:
                try:  
                    result = await sess.execute(
                        select(AccountInfo)
                    )    
                    return result.scalars().all()
                except Exception as E:
                    error_message = "Error while fetching all accounts."
                    logger.error(f"{error_message} Exception: {E}")
        return None
