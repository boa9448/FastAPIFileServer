from typing import Any
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import Depends, Request

from fastapi_file_server import exceptions, crud
from fastapi_file_server.database import get_db
from fastapi_file_server.libs import AUTHORIZATION, token


def LoginRedirectException(detail: Any, status_code: int = 302):
    return exceptions.RedirectException("/auth/login/", detail, status_code=status_code)


def UserInfoRedirectException(detail: Any, status_code: int = 302):
    return exceptions.RedirectException("/auth/info/", detail, status_code=status_code)


def token_required(requset: Request):
    return requset.session.get(AUTHORIZATION)


def set_token(requset: Request, token: str):
    requset.session[AUTHORIZATION] = token


def clear_token(requset: Request):
    requset.session.pop(AUTHORIZATION, None)


def get_current_user(auth_token:str = Depends(token_required), db: Session = Depends(get_db)):

    if not auth_token:
        raise LoginRedirectException("AuthTokenNotProvided")

    info = token.decode_token(auth_token)

    info_exp = info.get("exp")
    if not info_exp:
        raise LoginRedirectException("AuthTokenNotProvided")
    
    if info_exp < datetime.now().timestamp():
        raise LoginRedirectException("AuthTokenExpired")
    
    id_ = info.get("sub")
    db_user = crud.get_user(id_, db)
    
    return db_user


def active_required(db_user = Depends(get_current_user)):
    if not db_user.is_active:
        raise UserInfoRedirectException("UserIsNotActive")
    
    return db_user


def admin_required(db_user = Depends(get_current_user)):
    if not db_user.is_admin:
        raise UserInfoRedirectException("UserIsNotAdmin")
    
    return db_user