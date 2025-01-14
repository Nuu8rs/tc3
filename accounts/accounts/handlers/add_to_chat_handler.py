
from telethon.events.common import EventBuilder, EventCommon
from telethon.tl.types import UpdateChatParticipants, UpdateChannel , Chat, User, Channel

from accounts.bot.message_sender.succes_approved_chat import SendMessageSuccesApprovedChat

from database.models.projects import Project
from database.models.users import User
from database.models.invoice_pending_chat import InvoicePendingChat
from database.models.constans import EmptyList

from accounts.services.invoice_pending_chat_service import InvoicePendingChatService
from accounts.services.project_service import ProjectService
from accounts.services.telegram_chat_service import ChatTelegramService
from accounts.services.chat_association_service import ChatAssociationService
from accounts.services.project_chat_association_service import ProjceChatAssociationService

from typing import Union, Optional

class ChatParticipantsEvent(EventBuilder):
    def __init__(self, chats=None, *, blacklist_chats=False, func=None):
        super().__init__(chats, blacklist_chats=blacklist_chats, func=func)

    @classmethod
    def build(cls, update, others=None, self_id=None):
        if isinstance(update, (UpdateChatParticipants, UpdateChannel)):
            return cls.Event(update)
        return None

    class Event(EventCommon):
        def __init__(self, original_update):
            super().__init__()  
            self.original_update = original_update



class AddToChatHandler:
    def __init__(self, client, account_info, chat_manager) -> None:
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager

    async def handle(self, event: ChatParticipantsEvent.Event) -> None:
        enitities: dict[int, Union[Chat, User, Channel]] = event._entities 
        chat_value: Union[Chat,Channel] = next((value for value in enitities.values() if isinstance(value, (Chat, Channel))), None)
        chat_type: Optional[str] = None
        
        if not chat_value:
            return
        
        chat_name = chat_value.title
        chat_id = chat_value.id
        if isinstance(chat_value, Chat):
            chat_type = "CHANNEL"
        elif isinstance(chat_value, Channel):
            chat_type = "GROUP"

        if not any([chat_type, chat_id, chat_type]):
            return 

        if self.chat_manager.is_chat_allowed(chat_id):
            return 
        
        await self.approved_to_join(
            chat_name = chat_name,
            chat_id   = chat_id,
            chat_type = chat_type
        )
        
    async def approved_to_join(self, 
                               chat_name: str, 
                               chat_id: int,
                               chat_type: str
                              ):
        invoices_pending_chat: list[InvoicePendingChat] | EmptyList = await InvoicePendingChatService.get_chat_invoice(
            chat_name = chat_name
        )
        if not invoices_pending_chat:
            return
        for invoice_chat in invoices_pending_chat:
            project = await ProjectService.get_project(
                project_id = invoice_chat.project_id
            )
            if not project:
                continue
            
            bot_sender = SendMessageSuccesApprovedChat(
                project = project,
                chat_name = chat_name
            )
            
            await self.add_chat_to_views(
                invoice_chat = invoice_chat,
                chat_id      = chat_id,
                chat_type    = chat_type
            )
            await bot_sender.send_succes_join_chat()
            
            
    async def add_chat_to_views(self, 
                    invoice_chat: InvoicePendingChat,
                    chat_id: int,
                    chat_type: str
                    
                    ):
            tg_chat = await ChatTelegramService.add_new_chat(
                chat_link  = invoice_chat.chat_link,
                chat_name  = invoice_chat.chat_name,
                chat_id    = chat_id,
                chat_type  = chat_type,
            )
            if not tg_chat:
                return None
            
            await ChatAssociationService.add_new_association(
                account_id=self.account_info.id,
                chat_id=chat_id
            )

            await ProjceChatAssociationService.add_new_project_chat_association(
                chat_id    = chat_id,
                project_id = invoice_chat.project_id
            )

            await InvoicePendingChatService.delete_chat_invoice(
                invoice_id = invoice_chat.id
            )

            self.chat_manager.add_to_views_chat(
                chat_id=chat_id
            )
            