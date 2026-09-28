# PocketSmart AI — Budget & Recommendation Assistant

GenAI-powered budget planner for Home Interior, Party Planning, and Jewelry
recommendations, using Gemini 1.5 Flash to generate personalized, India-priced
suggestions with real shopping-site search links (Amazon, Flipkart, IKEA,
Swiggy, Zomato, OYO, Tanishq, etc.)

## Project structure

```
pocketsmart-ai/
├── main.py              # FastAPI app + all routes
├── auth.py               # password hashing, JWT, in-memory user/session store
├── models.py              # Pydantic request/response schemas
├── gemini_utils.py        # Gemini prompt building + the 3 recommendation engines
├── requirements.txt
├── .env.example            # copy to .env and fill in your key
├── templates/              # Jinja2 HTML pages
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── home_planner.html
│   ├── party_planner.html
│   ├── jewelry_planner.html
│   └── history.html
└── static/
    ├── css/style.css
    ├── js/main.js
    └── uploads/            # jewelry outfit photos land here
```

## Setup (run these in order)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# then open .env and paste your real GOOGLE_API_KEY
#   get one free at https://aistudio.google.com/app/apikey

# 4. Run the app
python main.py
# or: uvicorn main:app --reload
```

Open **http://localhost:8000** → it redirects to `/login` → click **Register**
to create an account → log in → you land on `/dashboard` with the three
planners + history.

## How it works
1. You submit a budget form (Home / Party / Jewelry).
2. The route in `main.py` builds a Pydantic model of your inputs and calls the
   matching function in `gemini_utils.py`.
3. That function builds a prompt, calls `model.generate_content(...)`
   (Gemini 1.5 Flash), and parses the JSON it returns.
4. Real search-URL links are attached per item (Amazon India, Flipkart, IKEA,
   Swiggy, Zomato, OYO, Tanishq, etc.) using the item's AI-generated
   `search_terms`.
5. The result is saved to that user's in-memory history and sent back to the
   page, which renders it as cards.

## Known limitations (same as the original project, worth mentioning in your report)
- **In-memory storage** — `users_db`, `active_sessions`, and history all live
  in Python dicts inside `auth.py`/`main.py`. Everything resets when the
  server restarts. Swap in SQLite/Postgres for anything beyond a demo.
- **No email verification** — registration just checks the username isn't
  taken.
- **Gemini output isn't 100% guaranteed valid JSON** — `extract_json_from_response()`
  strips markdown fences and does a best-effort parse, but a malformed
  response will still raise a 500.
- **CORS is wide open** (`allow_origins=["*"]`) — fine for local dev/demo,
  tighten before deploying anywhere public.

## If something doesn't run
- `ValueError: No Google API key found` → you haven't created `.env` or it's
  missing `GOOGLE_API_KEY`.
- `ModuleNotFoundError` → you didn't `pip install -r requirements.txt` inside
  the active virtual environment.
- Login works but pages instantly redirect back to `/login` → check that your
  browser isn't blocking cookies for `localhost`.
