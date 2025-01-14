from sqlalchemy import delete, select

from accounts.session import get_session
from database.models.invoice_pending_chat import InvoicePendingChat
from database.models.constans import EmptyList

from typing import Sequence

from accounts.logger.logger import logger

class InvoicePendingChatService:
    
    @classmethod
    async def add_new_invoice(cls, 
                              project_id: int, 
                              chat_name: str, 
                              chat_link: str
                              ) -> InvoicePendingChat | None:
        
        async for session in get_session():
            async with session as sess: 
                try:
                    new_invoice = InvoicePendingChat(
                        project_id = project_id,
                        chat_name = chat_name,
                        chat_link = chat_link
                    )
                    sess.add(new_invoice)
                    await sess.commit()
                    return new_invoice
                except Exception as E:
                    logger.error(f"Err {E} create new invoice\
                                 project_id = {project_id} |\
                                 chat_name = {chat_name}")
                    
        return None
    

    @classmethod
    async def get_chat_invoice(cls, chat_name: str) -> Sequence[InvoicePendingChat] | EmptyList:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        select(InvoicePendingChat)
                        .where(InvoicePendingChat.chat_name == chat_name)
                    )
                    result = await sess.execute(stmt)
                    
                    return result.scalars().all()
                except Exception as E:
                    logger.error(f"Err {E} fetch invoice chat_name: {chat_name}")
                    raise
                    
        return EmptyList()
    
    @classmethod
    async def delete_chat_invoice(cls, invoice_id: int) -> None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        delete(InvoicePendingChat)
                        .where(InvoicePendingChat.id == invoice_id)
                    )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    logger.error(f"Err {E} delete invoice invoice_id : {invoice_id}")
                    raise
        return None
    