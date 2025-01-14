from pydantic import BaseModel

class SendPost(BaseModel):
    post_id : int
    project_id: int
