from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from database.models.projects import Project


class ProjectRepository:
    @staticmethod
    async def get_project(
        tx: AsyncSession,
        project_id: int,
    ) -> Project | None:
        q = select(Project).where(
            Project.id == project_id
        )
        result = await tx.execute(q)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_project_by_user(
        tx: AsyncSession,
        user_id: int
    ) -> Sequence[Project]:
        q = select(Project).where(
            Project.user_id == user_id
        ).order_by(
            Project.creation_date
        )
        result = await tx.execute(q)
        return result.scalars().all()
