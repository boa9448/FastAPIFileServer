from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from fastapi_file_server.libs.session_depends import clear_token
from fastapi_file_server.templates import get_render, get_render_with_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/", response_class=HTMLResponse)
async def login(render = Depends(get_render)):
    return render("/auth/login.html")


@router.get("/logout/", response_class=HTMLResponse, dependencies=[Depends(clear_token)])
async def logout(render = Depends(get_render)):
    return render("/auth/login.html")


@router.get("/join/", response_class=HTMLResponse)
async def join(render = Depends(get_render)):
    return render("/auth/join.html")