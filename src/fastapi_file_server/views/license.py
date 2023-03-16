from fastapi import APIRouter, Depends

from fastapi_file_server.templates import get_render_with_user


verify_router = APIRouter()
router = APIRouter(prefix="/license", tags=["license"])


@router.get("/list/")
async def file_list(render = Depends(get_render_with_user)):
    return render("/license/list.html")


router.include_router(verify_router)