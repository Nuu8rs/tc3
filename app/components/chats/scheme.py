from pydantic import BaseModel, Field


class ChatInfoRequest(BaseModel):
    id: int = Field(..., description="Unical ID of the chat")


class AddChatRequest(BaseModel):
    url: str = Field(..., description="Invite link to the chat")


class AddChatResponse(BaseModel):
    status: str = Field("OK")
