from pydantic import BaseModel, Field, model_validator
from typing import Optional

from app.components.jinja2.filters import format_html


class PostInfoRequest(BaseModel):
    post_id: int = Field(..., description="Unical ID of the post")


class UpdatePostRequest(PostInfoRequest):
    text: str = Field(..., description="New text of post")

    @model_validator(mode="before")
    @classmethod
    def process_text(cls, values):
        if 'text' in values:
            values['text'] = format_html(values['text'])
        return values


class SendPostRequest(UpdatePostRequest):
    text: Optional[str] = Field(None, description="New text of post")


class SendPostResponse(BaseModel):
    status: str = Field(default="Ok")
    post_id: int


class UpdatePostResponse(SendPostResponse):
    post_id: int
