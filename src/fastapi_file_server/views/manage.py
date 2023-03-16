from fastapi import APIRouter, Depends

from fastapi_file_server.templates import get_render_with_user
from fastapi_file_server.libs.depends import admin_required


verify_router = APIRouter(dependencies=[Depends(admin_required)])
router = APIRouter(prefix="/manage", tags=["manage"])


@router.get("/user/list/")
async def user_list(render = Depends(get_render_with_user)):
    return render("/manage/user/list.html")


router.include_router(verify_router)