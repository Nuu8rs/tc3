from abc import ABC, abstractmethod
from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    detail: str | Exception
    status: int

    def __init__(self) -> None:
        super().__init__(self.status, self.detail)


class LogicError(Exception):
    pass


class DbEntityAlreadyExists(LogicError, ABC):
    detail: str = "already exists"

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """
        This property will be supplied by 
        the inheriting classes individually.
        """
        pass

    def __init__(self, name: str):
        super().__init__(f"{self.entity_name} {self.detail}: {name}")


class DbEntityNotFound(DbEntityAlreadyExists):
    detail: str = "not found"
