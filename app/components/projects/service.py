from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Sequence

from app.components.auth.scheme import TokenData
from app.components.projects.exceptions import InvalidProjectError
from app.components.projects.repo import ProjectRepository
from database.models.projects import Project


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepository
    ):
        self._project_repository = project_repository

    async def get_project(
        self,
        tx: AsyncSession,
        data: TokenData
    ) -> Project | None:
        if not data.current_project_id:
            return None
        project = await self.get_project_by_id(tx, data.current_project_id)
        if not project or project.user_id != data.user_id:
            raise InvalidProjectError()
        return project
    
    async def get_project_by_id(
        self,
        tx: AsyncSession,
        project_id: int
    ) -> Project | None:
        return await self._project_repository.get_project(
            tx, project_id
        )

    async def get_project_by_user(
        self,
        tx: AsyncSession,
        user_id: int
    ) -> Sequence[Project]:
        return await self._project_repository.get_project_by_user(
            tx, user_id
        )
