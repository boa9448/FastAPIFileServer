import os

from fastapi.templating import Jinja2Templates


cur_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(cur_dir, "templates")