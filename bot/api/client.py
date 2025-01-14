import asyncio
from aiohttp import (ClientTimeout, 
                     ClientSession, 
                     ClientResponse, 
                     ClientError, 
                     ClientResponseError, 
                     ClientConnectorError)

from bot.logger.logger import logger
from enum import Enum

from abc import ABC, abstractmethod
from typing import Union

class HttpMethods(Enum):
    GET  = "get"
    POST = "post"
    DELETE = "delete"


class Client(ABC):
    url = None
    method: HttpMethods.POST
    timeout = ClientTimeout(total=15)


    async def _request(self, url: str, **kwargs) -> Union[str, dict, None]:
        async with ClientSession(timeout=self.timeout) as session:
            try:
                async with session.request(method=self.method.value, url=url, **kwargs) as response:
                    content_type = response.headers.get('Content-Type', '')
                    
                    if 'application/json' in content_type:
                        response_answer = await response.json()
                    else:
                        response_answer = await response.text()
                    
                    logger.error(response_answer)
                    return response_answer
            except (ClientResponseError, ClientConnectorError, asyncio.TimeoutError, ClientError) as e:
                return self._handle_error(e)
            except Exception as e:
                return self._handle_error(e)


    def _handle_error(self, error: Exception) -> dict:
        error_message = {
            ClientResponseError: "Ошибка в ответе от сервера",
            ClientConnectorError: "Ошибка подключения к серверу",
            asyncio.TimeoutError: "Время ожидания запроса истекло",
            ClientError: "Общая ошибка клиента",
        }.get(type(error), "Неизвестная ошибка")

        logger.error(f"{error_message}: {error}")
        return {"status": "BAD", "message_error": f"{error_message}: {error}"}

        
    @abstractmethod
    async def send_response(self) -> ClientResponse:
        pass
        