from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from app.services.supabase_service import insert_hackathons
from app.models.hackathon import Hackathon
from urllib.parse import urljoin
      
def scrape_hackathon_data(hackathon_url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(hackathon_url, wait_until="networkidle")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    title = get_title(soup)
    tagline = get_tagline(soup) 
    date = get_date(soup)
    description = get_description(soup)
    team_size = get_team_size(soup)
    image_url = get_image_url(soup, hackathon_url)
    prize_pool = get_prize_pool(soup)
    location = get_location(soup)
    registration_cost = get_registration_cost(soup)
    

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
    
scrape_hackathon_data("https://hack-karnataka.devfolio.co/overview")
      
# if __name__ == "__main__":
#     scrape_hackathons()
