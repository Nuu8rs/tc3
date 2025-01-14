import traceback
from sqlalchemy import insert, select

from database.models.account_chat_association import AccountChatAssociation
from bot.session import get_session

from logger.logger import logger

class ChatAssociationService:
    @classmethod
    async def add_new_association(cls, 
                                  account_id: int, 
                                  chat_id: int) -> None:
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = insert(AccountChatAssociation).values(
                        chat_id = chat_id,
                        account_id = account_id
                        )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"<b>ERROR</b> add chat association account_id: {account_id} chat_id: {chat_id}"
                    
                    logger.error(f"{error_message}\nException: {E}")

                    
        
    @classmethod
    async def get_id_chats_by_account_id(cls, account_id: int) -> list[AccountChatAssociation]:
        async for session in get_session():
            async with session as sess:
                try:  
                    stmt = (
                        select(AccountChatAssociation)
                        .distinct()
                        .where(AccountChatAssociation.account_id == account_id))
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"<b>ERROR</b> get all chats from user account_id: <b>{account_id}</b>"
                    
                    logger.error(f"{error_message}\nException: {E}")
