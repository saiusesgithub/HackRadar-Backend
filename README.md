          ┌──────────────────┐
          │   Playwright     │
          │  (Get HTML data) │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  BeautifulSoup   │
          │ (Parse & organize│
          │   scraped data)  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │    Supabase      │
          │ (Store data in   │
          │  database)       │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │     FastAPI      │
          │ (Fetch from DB & │
          │ expose endpoints)│
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │     Flutter      │
          │ (App UI that     │
          │  consumes API)   │
          └──────────────────┘
