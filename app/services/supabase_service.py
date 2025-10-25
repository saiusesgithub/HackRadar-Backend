from supabase import create_client
from app.core.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_hackathons(hackathon_data):
    supabase.table("hackathons").insert(hackathon_data).execute()

def get_all_hackathons():
    response = supabase.table("hackathons").select("*").execute()
    return response.data
