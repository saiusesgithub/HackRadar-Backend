from fastapi import APIRouter
from app.services.supabase_service import get_all_hackathons

router = APIRouter(prefix="/hackathons", tags=["Hackathons"])

@router.get("/")
async def list_hackathons():
    return get_all_hackathons()
