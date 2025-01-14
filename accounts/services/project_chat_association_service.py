from sqlalchemy import select

from accounts.session import get_session
from database.models.chats import ProjectChatAssociation

from accounts.logger.logger import logger

class ProjceChatAssociationService:
    
    @classmethod
    async def get_association_projects_by_chat_id(cls, chat_id: int) -> list[ProjectChatAssociation] | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    
                    stmt = select(ProjectChatAssociation).where(ProjectChatAssociation.chat_id == chat_id)
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error fetching projects for chat_id: {chat_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None

    @classmethod
    async def add_new_project_chat_association(cls, chat_id: int, project_id: int):
        async for session in get_session():
            async with session as sess:  
                try:
                    project_chat_assoc = ProjectChatAssociation(
                        chat_id    = chat_id,
                        project_id = project_id
                    )
                    sess.add(project_chat_assoc)
                    await sess.commit()
                    return project_chat_assoc
                except Exception as E:
                    error_message = f"Error add new project chat association=  chat_id: {chat_id} | project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
                       