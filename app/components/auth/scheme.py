from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AuthTGModel(BaseModel):
    data: str

    
class ValidateTelegramData(BaseModel):
    valid: bool = True


class TokenData(BaseModel):
    user_id: int
    scopes: str
    exp: float
    telegram_id: Optional[int] = None
    current_project_id: Optional[int] = None