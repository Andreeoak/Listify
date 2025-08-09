from fastapi import  APIRouter

router = APIRouter()

@router.get("/auth/")
async def authUser():
    return {"message": "User Authenticated"}