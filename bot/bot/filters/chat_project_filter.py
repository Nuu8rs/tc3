import re
from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.models.projects import Project
from database.models.users import User

from datetime import datetime

from bot.services.project_service import ProjectService
from bot.services.user_service import UserService


class ChatProjectFilter(BaseFilter):
    pattern = r'Подписаться\s*$'

    async def __call__(self, event: Message) -> bool:
        if not event.chat:
            return False
        
        text = self._get_text(event)
        if not text:
            return False

        project: Project | None = await self._get_project(event.chat.id)
        if not project or not await self._is_user_subscription_active(project.user_id):
            return False

        return not re.search(self.pattern, text)

    def _get_text(self, event: Message) -> str | None:
        return event.text or event.caption

    async def _get_project(self, chat_id: int) -> Project | None:
        return await ProjectService.get_project_by_chat_id(chat_id=chat_id)

    async def _is_user_subscription_active(self, id_user: int) -> bool:
        user: User | None = await UserService.get_user(id_user=id_user)
        return True
        return bool(user and user.end_time_subscription > datetime.now())
        
        
        
        