from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer

from fastapi_file_server.libs import token, AUTHORIZATION
from fastapi_file_server.database import get_db
from fastapi_file_server import crud
from fastapi_file_server import exceptions


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/user/login/")
def token_required(token: str = Depends(oauth2_scheme)):
    return token


def get_current_user(auth_token:str = Depends(token_required), db: Session = Depends(get_db)):
    if not auth_token:
        raise exceptions.AuthTokenNotProvided()

    info = token.decode_token(auth_token)

    info_exp = info.get("exp")
    if not info_exp:
        raise exceptions.AuthTokenNotProvided()
    
    if info_exp < datetime.now().timestamp():
        raise exceptions.AuthTokenExpired()
    
    id_ = info.get("sub")
    db_user = crud.get_user(id_, db)
    
    return db_user


def active_required(db_user = Depends(get_current_user)):
    if not db_user.is_active:
        raise exceptions.UserIsNotActive()
    
    return db_user


def admin_required(db_user = Depends(get_current_user)):
    if not db_user.is_admin:
        raise exceptions.UserIsNotAdmin()
    
    return db_user