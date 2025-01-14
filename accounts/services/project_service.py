from sqlalchemy import insert, select
from accounts.session import get_session
from database.models.projects import Project

from accounts.logger.logger import logger

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