import os
from dotenv import load_dotenv
from supabase import create_client, Client
from app.models.hackathon import Hackathon

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def insert_hackathons(hackathons_data: Hackathon):
    supabase.table("open_hackathons").delete().neq("id", 0).execute()
    supabase.table("open_hackathons").insert(hackathons_data.dict()).execute()

def get_hackathons():
    response = supabase.table("open_hackathons").select("*").execute()
    return response.data


           








