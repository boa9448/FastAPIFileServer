from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_file_server.libs import token, AUTHORIZATION
from fastapi_file_server.database import get_db
from fastapi_file_server import crud
from fastapi_file_server import exceptions

class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict[str, str] = None,
        description: str = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        header_authorization = request.headers.get("Authorization")
        cookie_authorization = request.cookies.get(AUTHORIZATION)

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)

        #헤더와 쿠키 둘 중 하나라도 토큰이 있으면 토큰을 반환
        if header_authorization or cookie_authorization:
            if header_scheme.lower() == "bearer":
                return header_param
            elif cookie_scheme.lower() == "bearer":
                return cookie_param

        #헤더와 쿠키 둘 다 토큰이 없으면 에러
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return None


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/api/v1/auth/login/")
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