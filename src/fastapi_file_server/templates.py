from fastapi import Request
from fastapi.templating import Jinja2Templates

from fastapi_file_server import templates_dir


g_templates = Jinja2Templates(directory=templates_dir)


def get_render(request: Request):
    def _render(html_file: str, context: dict = {}):
        query_params = dict(request.query_params)
        path_params = dict(request.path_params)
        return g_templates.TemplateResponse(html_file, {"request": request
                                                        , "query_params": query_params
                                                        , "path_params": path_params
                                                        , **context})
    
    return _render