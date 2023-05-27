import os

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.exception_handlers import http_exception_handler

from fastapi_file_server import STATICS_DIR
from fastapi_file_server.database import create_db
from fastapi_file_server.config import get_config
from fastapi_file_server.exceptions import RedirectException
from fastapi_file_server.views.apis import (auth as api_auth
                                            , file as api_file
                                            , license as api_license)


def create_app() -> FastAPI:
    create_db()

    app = FastAPI()

    static = StaticFiles(directory = STATICS_DIR)
    app.mount("/static", static, name="static")

    app.include_router(api_auth.router)
    app.include_router(api_file.router)
    app.include_router(api_license.router)
    config = get_config()


    @app.on_event("startup")
    async def startup():
        file_dir = os.path.abspath(config.file_dir)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    
    @app.middleware("http")
    async def no_cache_middleware(request: Request, call_next):
        response = await call_next(request)
        #no cache
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app