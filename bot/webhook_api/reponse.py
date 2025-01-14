from typing import Literal, Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    status: Literal['OK', 'BAD']
    message_error: Optional[str] = ""

    @property
    def is_success(self) -> bool:
        return self.status == "OK"
    
    
class ResponseSendPost(BaseResponse):
    pass