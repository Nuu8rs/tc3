from database.models.posts import Post, Media
from database.models.projects import Project
from database.models.chats import ProjectChatAssociation

from accounts.bot.message_sender.send_message import SendMessager

from accounts.services.project_chat_association_service import ProjceChatAssociationService
from accounts.services.project_service import ProjectService


class PostSender:
    
    def __init__(
        self,
        post: Post,
        media: list[Media] | Media | None
                ) -> None:
        
        self.post  = post
        self.media = media
        
    
    
    async def send_post_to_project(self):
        projects_associations: list[ProjectChatAssociation] = await ProjceChatAssociationService.get_association_projects_by_chat_id(
            chat_id=self.post.chat_id
        )
        if not projects_associations:
            return
        
        for project_association in projects_associations:
            project: Project = await ProjectService.get_project(
                project_id=project_association.project_id
            )
            if not project or not project_association.auto_post:
                continue
            
            await self._send_message(project)
            
    async def _send_message(self, project: Project) -> None:
        sender_messages = SendMessager(
            post    = self.post,
            project = project,
            media   = self.media
        )
        await sender_messages.send_message()