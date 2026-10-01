# PocketSmart AI — Complete Project

This implementation follows the supplied project documentation and standardizes the runnable backend on **FastAPI**, because the later milestones explicitly specify FastAPI routes and Uvicorn. The document also asks for mock/simulated sourcing, so this project uses a local catalog plus search links instead of pretending to have live Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO inventory.

## Features
- Registration, login, logout and JWT-backed session
- SQLite database and recommendation history
- Home planner: rooms, quantities, style and budget
- Party planner: guests, event type, city, venue and food
- Jewelry planner: occasion/outfit fields + optional image
- Gemini multimodal integration for jewelry images
- Automatic fallback recommendations when Gemini is unavailable
- Responsive Jinja2 frontend
- JSON API endpoints
- `/docs` Swagger UI
- Automated health test

## Windows / VS Code
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Put your Gemini API key in `.env`:
```text
GEMINI_API_KEY=your_key_here
SECRET_KEY=use-a-long-random-secret
```

Then run:
```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

API docs: `http://127.0.0.1:8000/docs`
Health: `http://127.0.0.1:8000/health`

Without a Gemini key, the complete UI still works using deterministic fallback recommendations.

## Test
```powershell
pytest -q
```

## Project structure
```text
app/
  main.py
  config.py
  db.py
  models.py
  security.py
  catalog.py
  routes/
    auth.py
    planners.py
    dashboard.py
  services/
    gemini_service.py
    recommendation_service.py
    fallback.py
templates/
static/css/style.css
tests/test_api.py
requirements.txt
.env.example
```

## API
- POST `/generate-home`
- POST `/generate-party`
- POST `/generate-jewelry`
- POST `/token`
- POST `/api/register`
- GET `/session-info`
- GET `/session-data`
- GET `/recommendations-details/{id}`
- GET `/history`

## Gemini model note
The supplied document names Gemini 1.5 Flash Pro. The project defaults to `gemini-2.5-flash` because model availability changes over time. You can override `GEMINI_MODEL` in `.env` with a model enabled for your API account.

For production, add CSRF protection, rate limiting, HTTPS-only cookies, stronger secret management and a production database.
