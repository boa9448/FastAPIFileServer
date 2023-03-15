from datetime import datetime

from fastapi_file_server import models, exceptions


def find_license(licenses: list[models.License], id_: int):
    for license in licenses:
        if license.id == id_:
            return license
    
    raise exceptions.LicenseNotFound()


def find_license_by_file_id(licenses: list[models.License], file_id: int):
    for license in licenses:
        if license.file_id == file_id:
            return license
    
    raise exceptions.LicenseNotFound()


def is_alive_license(license: models.License):
    is_valid = license.valid_date > datetime.now()
    is_active = license.is_active is True
    is_alive = is_valid and is_active
    return is_alive