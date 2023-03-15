from typing import Any
from datetime import datetime, timedelta

from jose import JWTError, jwt

from fastapi_file_server.config import get_config
from fastapi_file_server.exceptions import TokenDecodeException


config = get_config()
TOKEN_SECRET_KEY = config.token_secret_key
ALGORITHM = config.algorithm
ACCESS_TOKEN_EXPIRE_DAYS = config.access_token_expire_days


def create_token(data: dict, expire : timedelta | None = None) -> str:
    to_encode = data.copy()
    if expire:
        expire = datetime.now() + expire
    else:
        expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        if token is None:
            raise TokenDecodeException()

        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise TokenDecodeException()
    except JWTError as e:
        print(e)
        raise TokenDecodeException()

    return payload


def create_access_token(data: Any) -> str:
    return create_token({'sub': str(data)})


def decode_access_token(token: str) -> dict:
    if token is None:
        raise TokenDecodeException()

    if not token.startswith("Bearer "):
        raise TokenDecodeException()

    token = token.replace("Bearer ", "")
    return decode_token(token)