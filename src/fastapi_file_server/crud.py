import os
from uuid import uuid4

from sqlalchemy.orm import Session

from fastapi_file_server import models, schemas, exceptions
from fastapi_file_server.libs import hash


def get_user(id_: int, db: Session):
    db_user = db.query(models.User).filter(models.User.id == id_).first()
    if not db_user:
        raise exceptions.UserNotFound()
    
    return db_user


def get_user_by_user_id(user_id: str, db: Session):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        raise exceptions.UserNotFound()
    
    return db_user


def is_exist_user_by_user_id(user_id: str, db: Session):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        return False
    
    return True


def get_user_list_query(db: Session):
    return db.query(models.User)


def create_user(user_info: schemas.UserCreate, db: Session):
    if is_exist_user_by_user_id(user_info.user_id, db):
        raise exceptions.UserAlreadyExists()

    if user_info.password1 != user_info.password2:
        raise exceptions.PassWordNotMatch()

    password = hash.get_password_hash(user_info.password1)

    user = models.User(
        user_id=user_info.user_id,
        password=password,
        name=user_info.name,
        email=user_info.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(id_: int, user_info: schemas.UserUpdate, db: Session):
    db_user = get_user(id_, db)
    
    db_user.name = user_info.name
    db_user.email = user_info.email
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(id_: int, db: Session):
    db_user = get_user(id_, db)

    db.delete(db_user)
    db.commit()
    return db_user


def set_is_active_user(id_: int, is_active: bool, db: Session):
    db_user = get_user(id_, db)
    db_user.is_active = is_active
    
    db.commit()
    db.refresh(db_user)
    return db_user


def set_is_admin_user(id_: int, is_admin: bool, db: Session):
    db_user = get_user(id_, db)    
    db_user.is_admin = is_admin
    
    db.commit()
    db.refresh(db_user)
    return db_user


def get_file(id_: int, db: Session):
    db_file = db.query(models.File).filter(models.File.id == id_).first()
    if not db_file:
        raise exceptions.FileNotFound()
    
    return db_file


def get_file_by_name(name: str, db: Session):
    db_file = db.query(models.File).filter(models.File.name == name).first()
    if not db_file:
        raise exceptions.FileNotFound()
    
    return db_file


def get_file_list_query(db: Session):
    return db.query(models.File)


def create_file(file_info: schemas.FileCreate, db: Session):
    ext = os.path.splitext(file_info.name)[-1]
    save_name = f"{uuid4()}{ext}"

    file = models.File(
        name=file_info.name,
        save_name=save_name,
        size=file_info.size,
        is_active=file_info.is_active,
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def delete_file(id_: int, db: Session):
    db_file = get_file(id_, db)

    db.delete(db_file)
    db.commit()
    return db_file


def set_is_active_file(id_: int, is_active: bool, db: Session):
    db_file = get_file(id_, db)
    db_file.is_active = is_active
    
    db.commit()
    db.refresh(db_file)
    return db_file


def get_license(id_: int, db: Session):
    db_license = db.query(models.License).filter(models.License.id == id_).first()
    if not db_license:
        raise exceptions.LicenseNotFound()
    
    return db_license


def get_license_list_query(db: Session):
    return db.query(models.License)


def create_license(license_info: schemas.LicenseCreate, db: Session):
    license = models.License(
        name=license_info.name,
        user_id=license_info.user_id,
        file_id=license_info.file_id,
        is_active=license_info.is_active,
        valid_date=license_info.valid_date,
    )
    db.add(license)
    db.commit()
    db.refresh(license)
    return license


def delete_license(id_: int, db: Session):
    db_license = get_license(id_, db)

    db.delete(db_license)
    db.commit()
    return db_license


def update_license(id_: int, license_info: schemas.LicenseUpdate, db: Session):
    db_license = get_license(id_, db)
    
    db_license.name = license_info.name
    db_license.is_active = license_info.is_active
    db_license.valid_date = license_info.valid_date
    
    db.commit()
    db.refresh(db_license)
    return db_license


def set_is_active_license(id_: int, is_active: bool, db: Session):
    db_license = get_license(id_, db)
    db_license.is_active = is_active
    
    db.commit()
    db.refresh(db_license)
    return db_license