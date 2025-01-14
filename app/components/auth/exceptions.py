from fastapi import status

from app.components.base.exceptions import BaseHTTPException


class BaseAuthException(BaseHTTPException):
    status: int = status.HTTP_401_UNAUTHORIZED


class AuthException(BaseAuthException):
    detail: str = "Not authenticated"


class CredentialsException(BaseAuthException):
    detail: str = "Could not validate credentials"


class PermissionsException(BaseAuthException):
    detail: str = "Not enough permissions"


class TgValidationException(BaseAuthException):
    detail: str = "Invalid auth data"


class PasswordException(BaseAuthException):
    detail: str = "Invalid password"


class NoTokenException(BaseAuthException):
    detail: str = "No token"


class InvalidTokenDataException(BaseAuthException):
    detail: str = "Invalid token"


class TokenDecodeException(BaseAuthException):
    detail: str = "Invalid token"
