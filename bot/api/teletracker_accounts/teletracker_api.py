from aiohttp import ClientResponse
from bot.api.client import Client, HttpMethods
from bot.api.schemas import ResponseAddAccount, BaseResponse

from bot.logger.logger import logger

from bot.config import config

class AddChatToAccount(Client):
    method = HttpMethods.POST
    url    = "/add-chat-to-account"
    
    def __init__(self, chat_link: str, project_id: int) -> None:
        self.chat_link = chat_link
        self.project_id = project_id
    
    async def send_response(self) -> ResponseAddAccount:
        try:
            url = config.BASE_API_URL + self.url
            
            data = {
                "chat_link"  : self.chat_link,
                "project_id" : self.project_id
            }
            
            response = await self._request(
                url  = url, 
                json = data
            )
            logger.info(response)
            return ResponseAddAccount(**response)
        
        except Exception as E:
            logger.error(E)
            return ResponseAddAccount(
                status="BAD",
                message_join_result="Произошел сбой при запрос при подключению к чату {chat_link}",
            )
            

class DeleteChatViews(Client):
    method = HttpMethods.DELETE
    url    = "/delete-chat-views"
    
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        
    async def send_response(self) -> BaseResponse:
        url = config.BASE_API_URL + self.url
        
        data = {
            "chat_id" : self.chat_id
        }
        response = await self._request(
            url = url,
            json = data
        )
        return BaseResponse(**response)