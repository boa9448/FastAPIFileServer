import os
from datetime import datetime

import aiofiles
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.responses import FileResponse
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_file_server import schemas, crud, models, exceptions
from fastapi_file_server.config import get_config
from fastapi_file_server.database import get_db
from fastapi_file_server.libs import token
from fastapi_file_server.libs.license import is_alive_license
from fastapi_file_server.libs.depends import admin_required


vrify_router = APIRouter(dependencies=[Depends(admin_required)])
un_vrify_router = APIRouter()
router = APIRouter(prefix="/api/v1/file", tags=["file"])
FILE_DIR = os.path.abspath(get_config().file_dir)


@vrify_router.get("/list/", response_model=Page[schemas.File])
async def list_file(db: Session = Depends(get_db)):
    file_query = crud.get_file_list_query(db)
    return paginate(file_query)


@un_vrify_router.get("/download/{id_}/", response_class=FileResponse)
async def download_file(id_: int
                        , license_token: str = Query()
                        , db: Session = Depends(get_db)):
    decode_license_token = token.decode_token(license_token)
    license_id = int(decode_license_token.get("sub"))
    db_license = crud.get_license(license_id, db)
    is_alive = is_alive_license(db_license) and db_license.file_id == id_
    if is_alive is False:
        raise exceptions.FileNotFound()

    db_file = crud.get_file(id_, db)
    file_name = db_file.save_name
    file_path = os.path.join(FILE_DIR, file_name)
    return FileResponse(file_path, filename=db_file.name)


@vrify_router.post("/upload/", response_model=schemas.File)
async def upload_file(upload_file: UploadFile, db: Session = Depends(get_db)):
    file_info = schemas.FileCreate(name=upload_file.filename
                                , size=upload_file.size
                                , is_active=False)
    db_file = crud.create_file(file_info, db)
    file = schemas.File.from_orm(db_file)

    file_name = file.save_name
    file_path = os.path.join(FILE_DIR, file_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await upload_file.read())

    return file


@vrify_router.delete("/delete/{id_}/", response_model=schemas.File)
async def delete_file(id_: int, db: Session = Depends(get_db)):
    db_file = crud.delete_file(id_, db)
    file = schemas.File.from_orm(db_file)

    file_name = file.save_name
    file_path = os.path.join(FILE_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    return file


@vrify_router.patch("/active/{id_}/", response_model=schemas.File)
async def file_set_is_active(id_: int, is_active: bool, db: Session = Depends(get_db)):
    db_file = crud.set_is_active_file(id_, is_active, db)
    file = schemas.File.from_orm(db_file)
    return file


router.include_router(un_vrify_router)
router.include_router(vrify_router)
add_pagination(router)