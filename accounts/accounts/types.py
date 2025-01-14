from dataclasses import dataclass
from typing import Optional, Union

from telethon.tl.types import Channel, Chat

from enum import Enum

class ResultJoin(Enum):
    SUCCES_JOIN  = "SUCCES_JOIN"
    ALREADY_JOIN = "ALREADY_JOIN"
    FAILED_JOIN  = "FAILED_JOIN"

class StatusDowloadMedia(Enum):
    DOWNLOADING = "DOWNLOADING"
    NOT_DOWNLOADING = "NOT_DOWNLOADING" 
    

@dataclass
class ResultJoinToChat:
    message_answer: str
    join_status: ResultJoin
    type_chat: Optional[str] = None
    chat: Optional[Union[Channel, Chat]] = None

    @property
    def current_chat(self) -> Union[Channel, Chat]:
        if hasattr(self.chat, "chats"):
            return self.chat.chats[0]
        return self.chat
    @property
    def chat_id(self) -> int | None:
        if self.chat:
            return self.current_chat.id
        return None
    
    @property
    def chat_title(self) -> str | None:
        if self.chat:
            return self.current_chat.title
        return None