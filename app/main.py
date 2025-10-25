from fastapi import FastAPI
from app.services.supabase_service import get_hackathons

app = FastAPI(title="Hackathon Scraper API")

@app.get("/hackathons")
async def hackathons():
    return get_hackathons()

