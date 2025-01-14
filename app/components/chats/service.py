from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Sequence

from app.components.auth.scheme import TokenData
from app.components.chats.repo import ChatRepository
from app.components.projects.service import ProjectService
from database.models.chats import Chat


class ChatService:
    def __init__(
        self, 
        chat_repository: ChatRepository,
        project_service: ProjectService
    ):
        self._chat_repository = chat_repository
        self._project_service = project_service

    async def get_chats(self, tx: AsyncSession, data: TokenData) -> Sequence[Chat]:
        project = await self._project_service.get_project(
            tx, data
        )
        if project is None:
            return ()
        
        chats_by_project = await self._chat_repository.get_chats_by_project(
            tx, project.id
        )
        if not chats_by_project:
            return ()
        
        chat_ids = [chat.chat_id for chat in chats_by_project]
        return await self._chat_repository.get_chats(tx, chat_ids)
    
    async def get_chat(
        self,
        tx: AsyncSession,
        chat_id: int,
        data: TokenData
    ) -> Chat | None:
        chats = await self.get_chats(tx, data)
        if not chats:
            return None
        
        for chat in chats:
            if chat.chat_id == chat_id:
                return await self._chat_repository.get_chat(tx, chat_id)
        else:
            return None
    