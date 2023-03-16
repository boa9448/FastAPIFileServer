from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse

from fastapi_file_server.libs import AUTHORIZATION
from fastapi_file_server.templates import get_render, get_render_with_user
from fastapi_file_server.exceptions import RedirectException


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/", response_class=HTMLResponse)
async def login(render = Depends(get_render)):
    return render("/auth/login.html")


@router.get("/logout/", response_class=HTMLResponse)
async def logout(response: Response, render = Depends(get_render)):
    response.delete_cookie(AUTHORIZATION)
    return render("/auth/logout.html")


@router.get("/join/", response_class=HTMLResponse)
async def join(render = Depends(get_render)):
    return render("/auth/join.html")


@router.get("/me/", response_class=HTMLResponse)
async def me(render = Depends(get_render_with_user)):
    return render("/auth/me.html")


@router.get("/password/edit/", response_class=HTMLResponse)
async def password_edit(render = Depends(get_render_with_user)):
    return render("/auth/password_edit.html")