from telethon import TelegramClient, events
from telethon.events.common import EventBuilder
from telethon.tl.types import UpdateChatParticipants

from database.models.account_info import AccountInfo

from accounts.accounts.handlers.new_message_handler import NewMessageHandler
from accounts.accounts.handlers.edit_message_handler import MessageEditHandler
from accounts.accounts.handlers.delete_message_handler import MessageDeleteHandler
from accounts.accounts.handlers.raw_handler import RawHandler
from accounts.accounts.handlers.add_to_chat_handler import AddToChatHandler, ChatParticipantsEvent


class ChatEvents:

    def __init__(
        self, 
        client: TelegramClient, 
        account_info: AccountInfo, 
        chat_manager
                ) -> None:
        
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager
        
    def register_handlers(self) -> None:
        self.client.on(events.NewMessage)(NewMessageHandler(self.client, self.account_info, self.chat_manager).handle)
        self.client.on(events.MessageEdited)(MessageEditHandler(self.client, self.account_info, self.chat_manager).handle)
        self.client.on(events.MessageDeleted)(MessageDeleteHandler(self.client, self.account_info, self.chat_manager).handle)
        
        # self.client.on(events.Raw)(RawHandler(self.client, self.account_info, self.chat_manager).handle)

        
        self.client.add_event_handler(
            AddToChatHandler(self.client, self.account_info, self.chat_manager).handle, 
            ChatParticipantsEvent()
        )


