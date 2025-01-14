from fastapi import status

from app.components.base.exceptions import BaseHTTPException


class BaseMediaException(BaseHTTPException):
    status: int = status.HTTP_400_BAD_REQUEST


class InvalidMediaException(BaseMediaException):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__()


class AddMediaException(BaseMediaException):
    detail: str = "Not enought rihgts to add media to this post"


class DeleteMediaException(BaseMediaException):
    detail: str = "Not enought rihgts to delete media of this post"
