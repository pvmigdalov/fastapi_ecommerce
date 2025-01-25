from fastapi import APIRouter

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
async def get_all_categories():
    pass

@router.post("/")
async def create_actegory():
    pass

@router.put("/")
async def update_category():
    pass

@router.delete("/")
async def delete_category():
    pass