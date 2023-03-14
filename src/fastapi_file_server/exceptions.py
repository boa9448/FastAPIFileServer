from typing import Any

from fastapi.exceptions import HTTPException


class BaseException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PassWordNotMatch(BaseException):
    def __init__(self):
        super().__init__(status_code=400, detail="Password not match")


class UserAlreadyExists(BaseException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists")


class UserNotFound(BaseException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class AuthTokenNotProvided(BaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="Auth token not provided")


class AuthTokenExpired(BaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="Auth token expired")


class UserIsNotActive(BaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="User is not active")


class UserIsNotAdmin(BaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="User is not admin")


class TokenDecodeException(BaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="Token is empty")


class FileNotFound(BaseException):
    def __init__(self):
        super().__init__(status_code=404, detail="File not found")