from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
router = APIRouter(prefix="/users", tags=["users"])
@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user