from fastapi import Request
from fastapi.templating import Jinja2Templates

from fastapi_file_server import templates_dir


g_templates = Jinja2Templates(directory=templates_dir)


def get_render(request: Request):
    def _render(html_file: str, context: dict = {}):
        return g_templates.TemplateResponse(html_file, {"request": request, **context})
    
    return _render