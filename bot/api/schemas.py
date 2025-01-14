from pydantic import BaseModel
from typing import Literal, Optional

class BaseResponse(BaseModel):
    status: Literal['OK', 'BAD']
    message_error: Optional[str] = None
    
    @property
    def is_succes(self) -> bool:
        return True if self.status == "OK" else False
    
class ResponseAddAccount(BaseResponse):
    message_join_result: str
    chat_id: Optional[int] = None
    project_id : Optional[int] = None 
    message_error: Optional[str] = None

