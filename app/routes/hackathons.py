from fastapi import APIRouter
from app.services.supabase_service import get_all_hackathons, get_hackathons

router = APIRouter(prefix="/hackathons", tags=["Hackathons"])

@router.get("/get_hackathons")
async def list_hackathons():
    return get_hackathons()
