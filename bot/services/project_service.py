from sqlalchemy import delete, select

from database.models.projects import Project
from bot.session import get_session

from bot.logger.logger import logger

class ProjectService:
    
    @classmethod
    async def get_project(cls, project_id: int) -> Project | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(Project).where(Project.id == project_id)
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error fetching project with project_id: {project_id}"
                    logger.error(f"{error_message}\nException: {E}")
            return None
    
    @classmethod
    async def get_projects_from_user(cls, id_user: int) -> list[Project] | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt   = select(Project).where(Project.user_id == id_user)
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error fetching projects with id_user: {id_user}"
                    logger.error(f"{error_message}\nException: {E}")
        return None
                    
    
    @classmethod
    async def add_new_project(cls, id_user: int, chat_id: int, chat_name: str) -> Project:
        async for session in get_session():
            async with session as sess: 
                try:
                    project_obj = Project(
                        user_id   = id_user,
                        chat_id   = chat_id,
                        chat_name = chat_name
                    )
                    sess.add(project_obj)
                    await sess.commit()
                    return project_obj
                except Exception as E:
                    ...
        return None

    @classmethod
    async def get_all_projects(cls) -> list[Project] | list:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(Project)
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error fetching all projects"
                    logger.error(f"{error_message}\nException: {E}")
        return list()
    
    
    @classmethod
    async def get_project_by_chat_id(cls, chat_id: int) -> Project | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (select(Project)
                            .where(Project.chat_id == chat_id))
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error fetching project from chat_id = {chat_id}"
                    logger.error(f"{error_message}\nException: {E}")
                    
    @classmethod
    async def delete_project(cls, project_id: int) -> None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = (
                        delete(Project)
                        .where(Project.id == project_id)
                        )
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    error_message = f"Error delete project from project_id = {project_id}"
                    logger.error(f"{error_message}\nException: {E}")