import os

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

from fastapi_file_server.database import create_db
from fastapi_file_server.templates import get_render
from fastapi_file_server.config import get_config
from fastapi_file_server.views.apis import auth as api_auth
from fastapi_file_server.views.apis import file as api_file


def create_app() -> FastAPI:
    create_db()

    app = FastAPI()
    app.include_router(api_auth.router)
    app.include_router(api_file.router)


    @app.on_event("startup")
    async def startup():
        config = get_config()
        file_dir = os.path.abspath(config.file_dir)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


    @app.get("/", response_class=HTMLResponse)
    async def index(render = Depends(get_render)):
        return render("index.html")

    return app