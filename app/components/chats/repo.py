from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from database.models.chats import Chat, ProjectChatAssociation


class ChatRepository:
    @staticmethod
    async def get_chat(
        tx: AsyncSession,
        chat_id: int
    ) -> Chat:
        q = select(Chat).where(
            Chat.chat_id == chat_id
        )
        result = await tx.execute(q)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_chats(
        tx: AsyncSession,
        chat_ids: list[int]
    ) -> Sequence[Chat]:
        q = select(Chat).where(
            Chat.chat_id.in_(chat_ids)
        )
        result = await tx.execute(q)
        return result.scalars().all()
    
    @staticmethod
    async def get_chats_by_project(
        tx: AsyncSession,
        project_id: int
    ) -> Sequence[ProjectChatAssociation]:
        q = select(ProjectChatAssociation).where(
            ProjectChatAssociation.project_id == project_id
        )
        result = await tx.execute(q)
        return result.scalars().all()

    