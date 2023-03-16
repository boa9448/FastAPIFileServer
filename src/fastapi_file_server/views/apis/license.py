from datetime import datetime

from sqlalchemy.orm import Session, Query
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy

from fastapi_file_server import crud, schemas, models, exceptions
from fastapi_file_server.database import get_db
from fastapi_file_server.libs import token
from fastapi_file_server.libs.license import find_license, is_alive_license
from fastapi_file_server.libs.depends import admin_required, active_required, get_current_user


verify_router = APIRouter(dependencies=[Depends(admin_required)])
un_verify_router = APIRouter()
router = APIRouter(prefix="/api/v1/license", tags=["license"], dependencies=[Depends(active_required)])


@router.get("/list/", response_model=Page[schemas.License])
async def license_list(db_user: models.User = Depends(get_current_user)):
    return paginate(db_user.licenses)


@router.get("/token/{id_}")
async def license_token(id_: int, db_user: models.User = Depends(get_current_user)):
    licenses = db_user.licenses
    db_license = find_license(licenses, id_)
    is_alive = is_alive_license(db_license)
    if is_alive is False:
        raise exceptions.LicenseNotFound()
    
    license_token = token.create_token({"sub": str(db_license.id)})
    return {"license_token": license_token}


@un_verify_router.get("/check/")
async def license_check(licence_token: str, db: Session = Depends(get_db)):
    decoded_token = token.decode_token(licence_token)
    id_ = decoded_token.get("sub")
    db_license = crud.get_license(id_, db)
    if db_license is None:
        raise exceptions.LicenseNotFound()
    
    is_alive = is_alive_license(db_license)
    return {"is_active": db_license.is_active
            , "valid_date": db_license.valid_date
            , "is_alive": is_alive}


@verify_router.post("/create/", response_model=schemas.License)
async def license_create(license_info: schemas.LicenseCreate, db: Session = Depends(get_db)):
    db_license = crud.create_license(license_info, db)
    license = schemas.License.from_orm(db_license)
    return license


@verify_router.post("/delete/{id_}", response_model=schemas.License)
async def license_delete(id_: int, db: Session = Depends(get_db)):
    db_license = crud.delete_license(id_, db)
    license = schemas.License.from_orm(db_license)
    return license


@verify_router.patch("/update/{id_}", response_model=schemas.License)
async def license_update(id_: int, license_info: schemas.LicenseUpdate, db: Session = Depends(get_db)):
    db_license = crud.update_license(id_, license_info, db)
    license = schemas.License.from_orm(db_license)
    return license


@verify_router.post("/active/{id_}", response_model=schemas.License)
async def license_active(id_: int, is_active: bool, db: Session = Depends(get_db)):
    db_license = crud.set_is_active_license(id_, is_active, db)
    license = schemas.License.from_orm(db_license)
    return license


router.include_router(un_verify_router)
router.include_router(verify_router)
add_pagination(router)