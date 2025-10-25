from pydantic import BaseModel

class Hackathon(BaseModel):
    title: str
    date: str
    link: str
    type: str
    no_of_participants: str