from aiohttp.web import Request, Response

from .base_endpoint import EndPoint, HTTPMethod, ResponseAnswer
from .schemas import SendPost
from .exceptions import ErrorResponse
from .reponse import ResponseSendPost

from database.models.posts import Post, Media
from database.models.projects import Project

from bot.config import config
from bot.bot.functions.sender_message_post import SenderPostsToProject
from bot.logger.logger import logger
from bot.services.post_service import PostService
from bot.services.project_service import ProjectService
from bot.services.media_service import MediaService

from typing import Union, Optional

class SendPostHandler(EndPoint):
    schema = SendPost
    method = HTTPMethod.POST
    data: SendPost = None
    
    async def handle_request(self) -> Response:
        bearer_token: str | None =  self.bearer_token()
        if not bearer_token:
            raise ErrorResponse(
                reason = "not token",
                status_code = 401
            )
        
        if bearer_token != config.AUTH_SECRET_KEY:
            
            raise ErrorResponse(
                reason = "not valide token",
                status_code = 401
            )

        post: Post = await PostService.get_post(
            post_id = self.data.post_id
        )
        if not post:
            raise ErrorResponse(
                reason = "not find post",
                status_code = 404
            )
        project: Project = await ProjectService.get_project(
            project_id = self.data.project_id
        )
        if not project:
            raise ErrorResponse(
                reason = "not find project",
                status_code = 404
            )

        await self._send_message(post, project)
        
        return ResponseSendPost(status = "OK")
        
    async def _send_message(
        self, 
        post: Post,
        project: Project
    ) -> None:
        
        media: Optional[Union[list[Media], Media]] = (
            await MediaService.get_media_to_post(
                post_id = post.id
            )
        ) 
        if len(media) == 1:
            media = media[0]
        
        sender_post = SenderPostsToProject(
            post    = post,
            project = project,
            media   = media  
        )
        
        await sender_post.send_message()
        