from os import link
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from app.services.supabase_service import insert_hackathons
from app.models.hackathon import Hackathon
from urllib.parse import urljoin

def scrape_hackathon_data(title: str,start_date: str,hackathon_url: str,type: str,no_of_participants: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(hackathon_url, wait_until="networkidle")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    title = get_title(soup)
    tagline = get_tagline(soup) 
    duration_date = get_date(soup)
    description = get_description(soup)
    team_size = get_team_size(soup)
    image_url = get_image_url(soup, hackathon_url)
    prize_pool = get_prize_pool(soup)
    location = get_location(soup)
    registration_cost = get_registration_cost(soup)
    
    hackathon_data: Hackathon = Hackathon(
        title=title,
        start_date=start_date,
        link=hackathon_url,
        type=type,
        no_of_participants=no_of_participants,
        tagline=tagline,
        duration_date=duration_date,
        description=description,
        team_size=team_size,
        image_url=image_url,
        prize_pool=prize_pool,
        location=location,
        registration_cost=registration_cost
        )
    
    insert_hackathons(hackathon_data)
  
def get_location(soup):
        label = soup.find(text="Happening")
        if label:
            location_tag = label.find_next("p")
            if location_tag:
                return location_tag.text.strip()
        return "Not specified"
    
def get_registration_cost(soup):
        label = soup.find(text="Registration costs?")
        if label:
            reg_cost_tag = label.find_next("p")
            if reg_cost_tag:
                return reg_cost_tag.text.strip()
        return "Not specified"

def get_title(soup):
    title = soup.select_one("h1").text.strip()
    return title

def get_tagline(soup):
    tagline = soup.select_one(".sc-dkzDqf.kCyCoN").text.strip()
    return tagline

def get_date(soup):
    date = soup.select_one(".sc-hKMtZM.hYgQkO").text.strip()
    return date

def get_description(soup):
    description = soup.select_one("[class*='ReadMore__StyledBox']").text.strip()
    return description

def get_team_size(soup):
    team_size = soup.select_one(".sc-hKMtZM.iHjekU").text.strip()
    return team_size

def get_image_url(soup, hackathon_url: str):
    img_element = soup.select_one(".sc-hKMtZM.gynsEi img")
    image_url = urljoin(hackathon_url, img_element.get("src"))
    return image_url

def get_prize_pool(soup):
    prize_pool = soup.select_one("h2").text.strip()
    return prize_pool 


# if __name__ == "__main__":
#     scrape_hackathon_data()
