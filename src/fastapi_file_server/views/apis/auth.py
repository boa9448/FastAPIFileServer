from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_file_server import crud, schemas, exceptions, models
from fastapi_file_server.database import get_db
from fastapi_file_server.libs import hash, token, AUTHORIZATION
from fastapi_file_server.libs.depends import (token_required
                                                , admin_required
                                                , get_current_user)


vrify_router = APIRouter(dependencies=[Depends(admin_required)])
un_vrify_router = APIRouter()
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@un_vrify_router.post("/create/", response_model=schemas.User)
async def user_create(user_info : schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(user_info, db)
    user = schemas.User.from_orm(db_user)
    return user


@un_vrify_router.post("/login/")
async def user_login(user_info: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_id(user_info.user_id, db)
    if not hash.verify_password(user_info.password, db_user.password):
        raise exceptions.PassWordNotMatch()

    user_token = token.create_access_token(db_user.id)
    user_token = f"bearer {user_token}"
    response.headers[AUTHORIZATION] = user_token
    response.set_cookie(AUTHORIZATION, user_token, httponly=True, samesite="strict", secure=True)

    #empty response
    return {}


@un_vrify_router.post("/token/")
async def user_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_id(form_data.username, db)
    if not hash.verify_password(form_data.password, db_user.password):
        raise exceptions.PassWordNotMatch()

    user_token = token.create_access_token(db_user.id)
    cookie_token = f"bearer {user_token}"
    response.set_cookie(AUTHORIZATION, cookie_token, httponly=True, samesite="strict", secure=True)
    return {"access_token": user_token, "token_type": "bearer"}


@un_vrify_router.get("/logout/")
async def user_logout(response: Response):
    response.delete_cookie(AUTHORIZATION)
    return {}


@un_vrify_router.get("/me/", response_model=schemas.User, response_model_exclude={"password", "is_admin", "id"})
async def user_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@un_vrify_router.patch("/edit/", response_model=schemas.User)
async def user_edit(user_info: schemas.UserUpdate
                    , current_user: models.User = Depends(get_current_user)
                    , db: Session = Depends(get_db)):
    if not (user_info.password1 or user_info.password2):
        raise exceptions.PassWordNotMatch()

    if user_info.password1 != user_info.password2:
        raise exceptions.PassWordNotMatch()
    
    is_verify = hash.verify_password(user_info.password1, current_user.password)
    if not is_verify:
        raise exceptions.PassWordNotMatch()

    db_user = crud.update_user(current_user.id, user_info, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.get("/info/{id_}/", response_model=schemas.User)
async def user_info(id_: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(id, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/update/{id_}/", response_model=schemas.User)
async def user_update(id_: str, user_info: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(id, user_info, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.delete("/delete/{id_}/", response_model=schemas.User)
async def user_delete(id_: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(id, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/admin/{id_}/", response_model=schemas.User)
async def user_set_is_admin(id_: str, is_admin: bool, db: Session = Depends(get_db)):
    db_user = crud.set_is_admin_user(id, is_admin, db)
    user = schemas.User.from_orm(db_user)
    return user


@vrify_router.patch("/active/{id_}/", response_model=schemas.User)
async def user_set_is_active(id_: str, is_active: bool, db: Session = Depends(get_db)):
    db_user = crud.set_is_active_user(id, is_active, db)
    user = schemas.User.from_orm(db_user)
    return user


router.include_router(un_vrify_router)
router.include_router(vrify_router)
add_pagination(router)