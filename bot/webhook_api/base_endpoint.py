from aiohttp.web import Request, Response, json_response
from pydantic import BaseModel, ValidationError
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
from .reponse import BaseResponse
from .exceptions import ErrorResponse

from accounts.logger.logger import logger

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    
class ResponseAnswer:

    def OK(self, schema: BaseResponse):
        return json_response(schema.dict(), status=200)

    def BAD(self, err: str, status: int = 500):
        schema = BaseResponse(status="BAD", message_error=err)
        return json_response(schema.dict(), status=status)



class EndPoint(ABC, ResponseAnswer):
    request: Request
    
    schema: BaseModel
    method: HTTPMethod
    
    data: dict = None
    
    def __init__(self, request: Request) -> None:
        self.request = request
        self.data = None
        
    @abstractmethod
    async def handle_request(self) -> Response:
        pass
    
    
    @property
    def method_is_valid(self) -> bool:
        return self.request.method == self.method.value
    
    def bearer_token(self) -> str | None:
        authorization_header = self.request.headers.get("Authorization")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return False

        return authorization_header.split("Bearer ")[1]
        
    
    async def get_data(self) -> BaseModel:  
        try:
            data = await self.request.json()
            data = self.schema(**data)
            return data
        except ValidationError as E:
            return self.BAD("No valid data")
        
        except Exception as E:
            logger.error(E)
            return self.BAD("Bad request")
    
    @classmethod
    async def router(cls, request: Request) -> Response:
        try:
            obj = cls(request)
            
            if not obj.method_is_valid:
                return obj.BAD("Not valid method")
            
            obj.data = await obj.get_data()
            schema = await obj.handle_request()
            return obj.OK(schema)
        except ErrorResponse as E:
            return obj.BAD(E.reason , status= E.status_code)
        except Exception as E:
            logger.error(f"Error response : {E}")
            return obj.BAD(
                err = "Bad Request"
            )
        