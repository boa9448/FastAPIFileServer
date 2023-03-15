import os

import aiofiles
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_file_server import schemas, crud, models
from fastapi_file_server.config import get_config
from fastapi_file_server.database import get_db
from fastapi_file_server.libs.api_depends import (active_required
                                                  , admin_required
                                                  , get_user)


vrify_router = APIRouter(dependencies=[Depends(admin_required)])
router = APIRouter(prefix="/api/v1/file", tags=["file"], dependencies=[Depends(active_required)])
FILE_DIR = os.path.abspath(get_config().file_dir)


@router.get("/list/", response_model=Page[schemas.File])
async def list_files(db_user: models.User = Depends(get_user), db: Session = Depends(get_db)):
    file_query = crud.get_file_list_query(db)
    file_query = file_query.filter(models.File.is_active == True)
    return paginate(file_query)


@router.get("/download/{id_}/", response_class=FileResponse)
async def download_file(id_: int, db: Session = Depends(get_db)):
    db_file = crud.get_file(id_, db)
    file = schemas.File.from_orm(db_file)

    file_name = file.save_name
    file_path = os.path.join(FILE_DIR, file_name)

    return FileResponse(file_path, filename=file.name)


@vrify_router.get("/list/all/", response_model=Page[schemas.File])
async def list_all_files(db: Session = Depends(get_db)):
    file_query = crud.get_file_list_query(db)
    return paginate(file_query)


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


router.include_router(vrify_router)
add_pagination(router)