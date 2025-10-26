from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from app.services.supabase_service import insert_hackathons, delete_previous_hackathons_data
from app.models.hackathon import Hackathon
from app.services.scraping.hackathon_details_scraper import scrape_hackathon_data

def scrape_hackathons():
    print("🚀 Starting hackathon scraper...")
    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("📡 Navigating to Devfolio hackathons page...")
        page.goto("https://devfolio.co/hackathons/open", wait_until="networkidle")
        print("✅ Page loaded successfully!")

        # code for getting data from lazy loaded website
        print("⏬ Scrolling to load all hackathons...")
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
                print(f"   Scroll attempt {scroll_attempts}/{max_attempts} - no new content")
            else:
                scroll_attempts = 0  # reset if new content loaded
                print(f"   New content loaded at height: {current_height}px")
            previous_height = current_height

        print("✅ Scrolling complete!")
        html = page.content()
        browser.close()
        print("🔒 Browser closed")

    print("🔍 Parsing HTML content...")
    soup = BeautifulSoup(html, "html.parser")

    hackathon_cards = soup.select("div[class*='CompactHackathonCard']")
    print(f"📋 Found {len(hackathon_cards)} hackathon cards")
    
    print("🗑️  Deleting previous hackathon data from database...")
    delete_previous_hackathons_data()
    print("✅ Previous data deleted")
    
    print(f"\n{'='*60}")
    print("📝 Starting to process hackathon cards...")
    print(f"{'='*60}\n")
    
    for index, card in enumerate(hackathon_cards, 1):
        print(f"🔄 Processing card {index}/{len(hackathon_cards)}...")
        p_tags = card.find_all("p")
        
        title_tag = card.select_one("h3")
        title = title_tag.text.strip() if title_tag else "Untitled Hackathon"
        
        link_tag = card.select_one("a")
        link = link_tag["href"] if link_tag and link_tag.get("href") else None
        
        # Skip if no link is found
        if not link:
            print(f"   ⚠️  Skipping card {index} - no link found")
            continue
        
        print(f"   Title: {title}")
        print(f"   Link: {link}")

        type = "Not specified"
        for p_tag in p_tags:
            if "Offline" in p_tag.get_text() or "Online" in p_tag.get_text():
                type = p_tag.get_text(strip=True)
                break
        
        no_of_participants = "Not specified"
        for p_tag in p_tags:
            if "participating" in p_tag.get_text():
                no_of_participants = p_tag.get_text(strip=True)
                break
        
        date = "Date not specified"
        for p_tag in p_tags:
            if "Starts" in p_tag.get_text():
                date = p_tag.get_text(strip=True)
                break

        print(f"   📊 Extracted data - Type: {type}, Date: {date}, Participants: {no_of_participants}")
        print(f"   🔗 Fetching detailed information...")
        scrape_hackathon_data(title=title,start_date=date,hackathon_url=link,type=type,no_of_participants=no_of_participants)
        print(f"   ✅ Card {index} processed successfully!\n")
    
    print(f"\n{'='*60}")
    print(f"🎉 Scraping completed! Processed {len(hackathon_cards)} hackathons")
    print(f"{'='*60}\n")
            
if __name__ == "__main__":
    scrape_hackathons()
