from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

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
                scroll_attempts += 1  # nothing new loaded → increment
            else:
                scroll_attempts = 0  # reset if new content loaded
            previous_height = current_height

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    hackathon_cards = soup.select("div[class*='CompactHackathonCard']")
    hackathons = []
    for card in hackathon_cards:
        title = card.select_one("h3")
        date = card.select_one("time")
        link = card.select_one("a")

        if title and link:
            hackathons.append({
                "title": title.text.strip(),
                "date": date.text.strip() if date else "Date not specified",
                "link": link["href"],
            })

    print(f"Total hackathons scraped: {len(hackathons)}\n")
    for h in hackathons:
        print(h["title"], h["date"], h["link"])

if __name__ == "__main__":
    scrape_hackathons()
