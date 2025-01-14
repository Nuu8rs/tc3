from pydantic import BaseModel, Field
from typing import List


class DeleteFileRequest(BaseModel):
    url: str = Field(..., description="File url")
    post_id: int = Field(..., description="Post id")
    


class DeleteFileResponse(BaseModel):
    status: str = "Ok"
    post_id: int


class UploadFileResponse(BaseModel):
    urls: List[str]
    post_id: int