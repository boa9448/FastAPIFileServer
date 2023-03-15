from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates

from fastapi_file_server import TEMPLATES_DIR
from fastapi_file_server.libs.session_depends import get_current_user


g_templates = Jinja2Templates(directory=TEMPLATES_DIR)


def get_render(request: Request):
    def _render(html_file: str, context: dict = {}):
        query_params = dict(request.query_params)
        path_params = dict(request.path_params)
        return g_templates.TemplateResponse(html_file, {"request": request
                                                        , "query_params": query_params
                                                        , "path_params": path_params
                                                        , **context})
    
    return _render


def get_render_with_user(request: Request, db_user = Depends(get_current_user)):
    def _render(html_file:str, context: dict = {}):
        query_params = dict(request.query_params)
        path_params = dict(request.path_params)
        return g_templates.TemplateResponse(html_file, {"request": request
                                                        , "user": db_user
                                                        , "query_params": query_params
                                                        , "path_params": path_params
                                                        , **context})

    return _render