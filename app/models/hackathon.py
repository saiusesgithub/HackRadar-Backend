from pydantic import BaseModel

class Hackathon(BaseModel):
    title: str
    start_date: str
    link: str
    type: str
    no_of_participants: str
    tagline: str 
    duration_date: str
    description: str
    team_size: str
    image_url: str
    prize_pool: str
    location: str
    registration_cost: str