from fastapi import status

from app.components.base.exceptions import BaseHTTPException


class BasePostException(BaseHTTPException):
    status: int = status.HTTP_400_BAD_REQUEST


class PostNotFoundException(BasePostException):
    detail: str = "Post not found"
