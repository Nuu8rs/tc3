from sqlalchemy import update, select, delete

from database.models.chats import ProjectChatAssociation
from bot.session import get_session

from bot.bot.types import StatusAutopost

from bot.logger.logger import logger

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
    async def get_association_by_project_id(cls, project_id: int) -> list[ProjectChatAssociation] | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    
                    stmt = select(ProjectChatAssociation).where(ProjectChatAssociation.project_id == project_id)
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error fetching projects for project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
                    raise
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
                       
     
    @classmethod
    async def get_chat_association(cls, chat_id: int, project_id: int) -> ProjectChatAssociation | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (select(ProjectChatAssociation)
                            .where(ProjectChatAssociation.chat_id == chat_id)
                            .where(ProjectChatAssociation.project_id == project_id)
                            )
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error get project chat association = chat_id: {chat_id} | project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None
    

    @classmethod
    async def edit_status_autopost(cls, chat_id: int, project_id: int, status_auto_post: bool) -> None:
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (
                        update(ProjectChatAssociation)
                        .where(ProjectChatAssociation.chat_id    == chat_id)
                        .where(ProjectChatAssociation.project_id == project_id)
                        .values(auto_post = status_auto_post)
                        )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error update status autopost = chat_id: {chat_id} | project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
                    
    
    @classmethod
    async def delete_chat_from_project(cls, project_id: int, chat_id: int):
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (
                        delete(ProjectChatAssociation)
                        .where(ProjectChatAssociation.chat_id == chat_id)
                        .where(ProjectChatAssociation.project_id == project_id)
                    )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error delete chat from project  chat_id: {chat_id} | project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
                    
    @classmethod
    async def delete_association_from_project(cls, project_id: int):
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (
                        delete(ProjectChatAssociation)
                        .where(ProjectChatAssociation.id == project_id)
                    )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error project association  from project_id : {project_id}"
                    logger.error(f"{error_message}\nException: {E}")