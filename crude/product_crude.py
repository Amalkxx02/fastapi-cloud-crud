from fastapi import APIRouter,HTTPException

router = APIRouter(prefix="/",tags=["product"])

@router.get("")
async def product_get():
    pass

@router.post("")
async def product_post():
    pass

@router.put("")
async def product_put():
    pass

@router.patch("")
async def product_post():
    pass