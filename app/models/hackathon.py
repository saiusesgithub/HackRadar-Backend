from pydantic import BaseModel

class Hackathon(BaseModel):
    title: str
    link: str
    type: str
    no_of_participants: str
    start_date: str
    duration_date: str
    tagline: str 
    description: str
    team_size: str
    image_url: str
    prize_pool: str
    location: str
    registration_cost: str