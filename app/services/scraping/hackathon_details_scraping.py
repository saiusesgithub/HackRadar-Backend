from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright,expect
import time
from app.services.supabase_service import insert_hackathons, delete_previous_hackathons_data
from app.models.hackathon import Hackathon
import requests
from urllib.parse import urljoin
      
def scrape_hackathon_data(hackathon_url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(hackathon_url, wait_until="networkidle")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    
    title = soup.select_one("h1").text.strip()
    tagline = soup.select_one(".sc-dkzDqf.kCyCoN").text.strip()
    date = soup.select_one(".sc-hKMtZM.hYgQkO").text.strip()
    # location = soup.select_one(".sc-hKMtZM.hYgQkO").text.strip()
    # description = soup.select_one(".sc-dkzDqf.kCyCoN").text.strip()
    description = soup.select_one("[class*='ReadMore__StyledBox']").text.strip()
    team_size = soup.select_one(".sc-hKMtZM.iHjekU").text.strip()
    # registration_cost = soup.select_one(".sc-hKMtZM.iHjekU").text.strip()
    # prize_pool = soup.select_one(".sc-dkzDqf.hUqWTC")
    # simplest: get the <img> inside the container and absolutize its src
    img_element = soup.select_one(".sc-hKMtZM.gynsEi img")
    image_url = urljoin(hackathon_url, img_element.get("src"))
    prize_pool = soup.select_one("h2").text.strip()
    
    
    # def get_prize_pool(soup):
    #     label = soup.find(text="Prize Pool")
    #     if label:
    #         prize_pool_tag = label.find_next("p")
    #         if prize_pool_tag:
    #             return prize_pool_tag.text.strip()
    #     return "Not specified"

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
    
    # prize_pool = get_prize_pool(soup)
    location = get_location(soup)
    registration_cost = get_registration_cost(soup)
    
    
    # # getting the element which has the literal text - 'Prize Pool'
    # label = page.locator("text=Prize Pool").first
    # # Get the next <p> tag after the label
    # next_label = label.locator("xpath=following::p[1]")
    # prize_pool = next_label.text_content()

    # # getting the element which has the literal text - 'Happening'
    # label = page.locator("text=Happening").first
    # # Get the next <p> tag after the label
    # next_label = label.locator("xpath=following::p[1]")
    # location = next_label.text_content()

    # # getting the element which has the literal text - 'Registration costs'
    # label = page.locator("text=Registration costs").first
    # # Get the next <p> tag after the label
    # next_label = label.locator("xpath=following::p[1]")
    # registration_cost = next_label.text_content()

    # write this data to a file 
    output_lines = [
        f"Title: {title}",
        f"Tagline: {tagline}",
        f"Date: {date}",
        f"Location: {location}",
        f"Description: {description}",
        f"Team size: {team_size}",
        f"Registration cost: {registration_cost}",
        f"Prize pool: {prize_pool}",
        f"Image: {image_url}",
    ]

    out_path = "hackathon_details.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Saved hackathon details to {out_path}")

    
    # hackathon_cards = soup.select("div[class*='CompactHackathonCard']")
    
    # delete_previous_hackathons_data()
    
    # for card in hackathon_cards:
    #     p_tags = card.find_all("p")
    #     title = card.select_one("h3").text.strip()
    #     link = card.select_one("a")["href"]

    #     for p_tag in p_tags:
    #         if "Offline" in p_tag.get_text() or "Online" in p_tag.get_text():
    #             type = p_tag.get_text(strip=True)
    #             break
        
    #     for p_tag in p_tags:
    #         if "participating" in p_tag.get_text():
    #             no_of_participants = p_tag.get_text(strip=True)
    #             break
        
    #     for p_tag in p_tags:
    #         if "Starts" in p_tag.get_text():
    #             date = p_tag.get_text(strip=True)
    #             break      
    #     if not date:
    #         date = "Date not specified"

    #     hackathon_data: Hackathon = Hackathon(
    #         title=title,
    #         date=date,
    #         link=link,
    #         type=type,
    #         no_of_participants=no_of_participants
    #     )

    #     if title and type:
    #         insert_hackathons(hackathon_data)
  
    
scrape_hackathon_data("https://hack-karnataka.devfolio.co/overview")
      
# if __name__ == "__main__":
#     scrape_hackathons()
