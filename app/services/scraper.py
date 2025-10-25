from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_hackathons():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://devfolio.co/hackathons/open", wait_until="networkidle")
        html = page.content()
        browser.close()
    soup = BeautifulSoup(html, "html.parser")   

    cards = soup.select("div[class*='CompactHackathonCard']")
    for card in cards:
        title = card.select_one("h3") 
        date = card.select_one("time")  
        link = card.select_one("a")
        if title and link:
            title = title.text.strip()
            link = link["href"]
            date = date.text.strip() if date else "Date not specified"
            print(title, date, link)
