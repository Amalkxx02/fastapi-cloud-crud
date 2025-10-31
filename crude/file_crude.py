from fastapi import APIRouter,HTTPException

router = APIRouter(prefix="/",tags=["file"])

@router.get("")
async def file_get():
    pass

@router.post("")
async def file_post():
    pass

@router.put("")
async def file_put():
    pass

@router.patch("")
async def file_post():
    pass