from fastapi import FastAPI
from app.routes import hackathons

app = FastAPI(title="Hackathon Scraper API")

app.include_router(hackathons.router)
