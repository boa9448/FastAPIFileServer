from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/user/login/")
def token_required(token: str = Depends(oauth2_scheme)):
    return token