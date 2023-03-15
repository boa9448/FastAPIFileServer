import os

from fastapi.templating import Jinja2Templates


cur_dir = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(cur_dir, "templates")
STATICS_DIR = os.path.join(cur_dir, "statics")