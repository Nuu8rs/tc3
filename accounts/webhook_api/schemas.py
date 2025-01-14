from pydantic import BaseModel

class JoinToChatSchema(BaseModel):
    chat_link:  str
    project_id: int 
    
    
class DeleteChatFromPool(BaseModel):
    chat_id: int