from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from app.services.supabase_service import insert_hackathons, delete_previous_hackathons_data
from app.models.hackathon import Hackathon
from app.services.scraping.hackathon_details_scraper import scrape_hackathon_data

def scrape_hackathons():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://devfolio.co/hackathons/open", wait_until="networkidle")

        # code for getting data from lazy loaded website
        previous_height = 0
        scroll_attempts = 0
        max_attempts = 10 

        while scroll_attempts < max_attempts:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            # buffer time for the cards to load
            time.sleep(3) 
            
            # Check if page height changed
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                scroll_attempts += 1  # nothing new loaded then increment
            else:
                scroll_attempts = 0  # reset if new content loaded
            previous_height = current_height

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    hackathon_cards = soup.select("div[class*='CompactHackathonCard']")
    
    delete_previous_hackathons_data()
    
    for card in hackathon_cards:
        p_tags = card.find_all("p")
        title = card.select_one("h3").text.strip()
        link = card.select_one("a")["href"]

        for p_tag in p_tags:
            if "Offline" in p_tag.get_text() or "Online" in p_tag.get_text():
                type = p_tag.get_text(strip=True)
                break
        
        for p_tag in p_tags:
            if "participating" in p_tag.get_text():
                no_of_participants = p_tag.get_text(strip=True)
                break
        
        for p_tag in p_tags:
            if "Starts" in p_tag.get_text():
                date = p_tag.get_text(strip=True)
                break      
        if not date:
            date = "Date not specified"

        scrape_hackathon_data(title=title,start_date=date,hackathon_url=link,type=type,no_of_participants=no_of_participants)
            
if __name__ == "__main__":
    scrape_hackathons()
