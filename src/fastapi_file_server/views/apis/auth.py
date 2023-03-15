from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_file_server import crud, schemas, exceptions
from fastapi_file_server.database import get_db
from fastapi_file_server.libs import hash, token, AUTHORIZATION
from fastapi_file_server.libs import session_depends
from fastapi_file_server.libs.api_depends import (token_required
                                                , admin_required
                                                , get_current_user)


vrify_router = APIRouter(dependencies=[Depends(admin_required)])
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/user/create/", response_model=schemas.User)
async def user_create(user_info : schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(user_info, db)
    user = schemas.User.from_orm(db_user)
    return user


@router.post("/user/token/")
async def user_token(user_info: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_id(user_info.user_id, db)
    if not hash.verify_password(user_info.password, db_user.password):
        raise exceptions.PassWordNotMatch()

    user_token = token.create_access_token(db_user.id)
    response.headers[AUTHORIZATION] = f"bearer {user_token}"

    #empty response
    return {}


@router.post("/user/token/session/")
async def user_token_session(request: Request, user_info: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_id(user_info.user_id, db)
    if not hash.verify_password(user_info.password, db_user.password):
        raise exceptions.PassWordNotMatch()

    user_token = token.create_access_token(db_user.id)
    session_depends.set_token(request, user_token)

    return {"redirect_url": "/"}



@router.post("/user/login/")
async def user_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_id(form_data.username, db)
    if not hash.verify_password(form_data.password, db_user.password):
        raise exceptions.PassWordNotMatch()

    user_token = token.create_access_token(db_user.id)
    return {"access_token": user_token, "token_type": "bearer"}


@vrify_router.get("/user/info/{id_}/", response_model=schemas.User)
async def user_info(id_: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(id, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/user/update/{id_}/", response_model=schemas.User)
async def user_update(id_: str, user_info: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(id, user_info, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.delete("/user/delete/{id_}/", response_model=schemas.User)
async def user_delete(id_: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(id, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/user/admin/{id_}/", response_model=schemas.User)
async def user_set_is_admin(id_: str, is_admin: bool, db: Session = Depends(get_db)):
    db_user = crud.set_is_admin_user(id, is_admin, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/user/active/{id_}/", response_model=schemas.User)
async def user_set_is_active(id_: str, is_active: bool, db: Session = Depends(get_db)):
    db_user = crud.set_is_active_user(id, is_active, db)
    user = schemas.User.from_orm(db_user)
    return user


router.include_router(vrify_router)
add_pagination(router)