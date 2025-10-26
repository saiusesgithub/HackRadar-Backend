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
    duration_date = get_duration_date(soup)
    description = get_description(soup)
    team_size = get_team_size(soup)
    image_url = get_image_url(soup, hackathon_url,title)
    prize_pool = get_prize_pool(soup)
    location = get_location(soup)
    registration_cost = get_registration_cost(soup)
    
    hackathon_data: Hackathon = Hackathon(
        title=title,
        link=hackathon_url,
        type=type,
        no_of_participants=no_of_participants,
        start_date=start_date,
        duration_date=duration_date,
        tagline=tagline,
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
    title_tag = soup.select_one("h1")
    return title_tag.text.strip() if title_tag else "Untitled Hackathon"

def get_tagline(soup):
    element = soup.select_one("[class*='Overview__StyledMarkdown']")
    return element.get_text(strip=True) if element else "Not specified"

def get_duration_date(soup):
    label = soup.find(text="Runs from")
    if label:
        duration_date = label.find_next("p")
        if duration_date:
            return duration_date.text.strip()
    return "Not specified"

def get_description(soup):
    description_tag = soup.select_one("[class*='ReadMore__StyledBox']")
    return description_tag.text.strip() if description_tag else "Not specified"

def get_team_size(soup):
    label = soup.find(text="Team size")
    if label:
        team_size = label.find_next("p")
        if team_size:
            return team_size.text.strip()
    return "Not specified"

def get_image_url(soup, hackathon_url: str,title: str):
    image = soup.find("img", attrs={"alt": title})
    if not image:
        return "Not specified"
    src = image.get("src")
    return urljoin(hackathon_url, src) if src else "Not specified"

def get_prize_pool(soup):
    prize_pool_tag = soup.select_one("h2")
    return prize_pool_tag.text.strip() if prize_pool_tag else "Not specified" 


# if __name__ == "__main__":
#     scrape_hackathon_data()
