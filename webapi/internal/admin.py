from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/admin", tags=["admin"])
async def read_admin():
    return [{"username": "Rick"}, {"username": "Morty"}]