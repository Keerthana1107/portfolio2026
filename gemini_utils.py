"""
gemini_utils.py
Everything that talks to Gemini: prompt building, calling the model, parsing
its JSON response, and attaching real shopping-site search links.
"""

import os
import re
import json
import shutil
import urllib.parse
import uuid
from typing import Optional

from fastapi import HTTPException, UploadFile
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

from models import HomeBudgetInput, PartyBudgetInput, JewelryBudgetInput

# ---------- Load env + configure Gemini ----------

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    # Try alternative environment variable name
    API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "No Google API key found in environment variables. "
        "Please set GOOGLE_API_KEY in your .env file."
    )

genai.configure(api_key=API_KEY)

# "gemini-1.5-flash" is the current model id for what the doc calls
# "Gemini 1.5 Flash Pro". Change here if Google renames/deprecates it.
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------- Shared helpers ----------

def extract_json_from_response(text: str) -> dict:
    """
    Gemini sometimes wraps JSON in ```json ... ``` fences or adds stray text
    around it. Strip fences and grab the outermost {...} block, then parse.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"```\s*$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back: grab the first {...} block in the text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise HTTPException(500, "Could not parse AI response as JSON")


def save_upload_file(upload_file: UploadFile, upload_dir: str = "static/uploads") -> str:
    """Save an uploaded image to disk and return its path."""
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(upload_file.filename or "")[1] or ".png"
    filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(upload_dir, filename)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return dest_path


def usd_to_inr(amount_usd: float, exchange_rate: float = 83.0) -> float:
    """Convert USD amount to INR using the specified exchange rate"""
    return amount_usd * exchange_rate


# ---------- 1. Home Planner ----------

def get_home_recommendations(budget_input: HomeBudgetInput) -> dict:
    """Generate home interior recommendations within budget in INR for Indian market"""
    try:
        prompt = f"""
I need interior design product recommendations for a home in India with a total budget of ₹{budget_input.total_budget:.2f}.

Requirements:
- {budget_input.num_lights} lights/lighting fixtures
- {budget_input.num_fans} ceiling fans
- {budget_input.num_furniture} furniture pieces
- {budget_input.num_dining_tables} dining tables

Additional rooms to consider:
{("- Living room" if budget_input.has_living_room else "")}
{("- Kitchen" if budget_input.has_kitchen else "")}
{("- Bedroom" if budget_input.has_bedroom else "")}

Additional requirements: {budget_input.additional_requirements or "None"}

Please provide a detailed budget breakdown with product recommendations available in India.
Use Indian brands and pricing. Include search terms suitable for Indian shopping platforms.

Respond with ONLY valid JSON (no markdown fences) in exactly this structure:
{{
    "total_budget": {budget_input.total_budget:.2f},
    "budget_breakdown": [
        {{
            "category": "lighting",
            "allocation": 0.0,
            "items": [
                {{
                    "name": "",
                    "description": "",
                    "estimated_price": 0.0,
                    "quantity": 0,
                    "search_terms": ""
                }}
            ]
        }}
    ],
    "calculation_table": [
        {{
            "category": "",
            "items_count": 0,
            "total_cost": 0.0,
            "percentage_of_budget": 0.0
        }}
    ],
    "remaining_budget": 0.0,
    "additional_suggestions": []
}}

Ensure total costs stay within budget.
"""
        response = model.generate_content(prompt)
        result = extract_json_from_response(response.text)

        # Add shopping links for each item
        for category in result.get("budget_breakdown", []):
            for item in category.get("items", []):
                search_terms = item.get("search_terms", "")
                if search_terms:
                    item["shopping_links"] = {
                        "amazon": f"https://www.amazon.in/s?k={urllib.parse.quote_plus(search_terms)}",
                        "flipkart": f"https://www.flipkart.com/search?q={urllib.parse.quote_plus(search_terms)}",
                        "ikea": f"https://www.ikea.com/in/en/search/?q={urllib.parse.quote_plus(search_terms)}",
                        "myntra": f"https://www.myntra.com/search?q={urllib.parse.quote_plus(search_terms)}",
                        "ajio": f"https://www.ajio.com/search/?text={urllib.parse.quote_plus(search_terms)}",
                    }

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error generating recommendations: {str(e)}")


# ---------- 2. Party Planner ----------

def get_party_recommendations(budget_input: PartyBudgetInput) -> dict:
    """Generate party planning recommendations within budget in INR for Indian market"""
    try:
        prompt = f"""
I need party planning recommendations for India with a total budget of ₹{budget_input.total_budget:.2f}.

Party details:
- Type: {budget_input.party_type}
- Number of guests: {budget_input.num_guests}
- Venue type: {budget_input.venue_type or "Not specified"}
- Catering needed: {"Yes" if budget_input.needs_catering else "No"}
- Decoration needed: {"Yes" if budget_input.needs_decoration else "No"}
- Entertainment needed: {"Yes" if budget_input.needs_entertainment else "No"}

Additional requirements: {budget_input.additional_requirements or "None"}

Please provide a detailed budget breakdown with specific recommendations available in India
using INR prices. Use Indian brands, services, and typical cost expectations.

Respond with ONLY valid JSON (no markdown fences) in exactly this structure:
{{
    "total_budget": {budget_input.total_budget:.2f},
    "budget_breakdown": [
        {{
            "category": "venue",
            "allocation": 0.0,
            "items": [
                {{
                    "name": "",
                    "description": "",
                    "estimated_price": 0.0,
                    "quantity": 0,
                    "search_terms": ""
                }}
            ]
        }}
    ],
    "venue_suggestions": [
        {{
            "name": "",
            "type": "",
            "capacity": 0,
            "estimated_cost": 0.0,
            "search_terms": ""
        }}
    ],
    "remaining_budget": 0.0,
    "additional_suggestions": []
}}

Ensure all costs are in INR and total does not exceed the given budget.
"""
        response = model.generate_content(prompt)
        result = extract_json_from_response(response.text)

        # ---- Build an INR calculation table grouped by category ----
        result["calculation_table_inr"] = []
        categories = {}

        for category in result.get("budget_breakdown", []):
            cat_name = category.get("category", "Misc")
            if cat_name not in categories:
                categories[cat_name] = {
                    "category": cat_name,
                    "items_count": 0,
                    "total_cost": 0,
                    "percentage_of_budget": 0,
                }
            for item in category.get("items", []):
                categories[cat_name]["items_count"] += 1
                categories[cat_name]["total_cost"] += item.get("estimated_price", 0)

            if result.get("total_budget", 0) > 0:
                categories[cat_name]["percentage_of_budget"] = (
                    categories[cat_name]["total_cost"] / result["total_budget"]
                ) * 100

        for cat_data in categories.values():
            result["calculation_table_inr"].append(cat_data)

        # ---- Category -> relevant shopping platforms ----
        category_platforms = {
            "venue": ["google", "booking", "makemytrip", "oyorooms", "nobroker"],
            "catering": ["swiggy", "zomato"],
            "food": ["swiggy", "zomato", "bigbasket", "amazon", "flipkart"],
            "drinks": ["swiggy", "zomato", "bigbasket", "amazon", "flipkart"],
            "decoration": ["amazon", "flipkart", "meesho", "myntra"],
            "entertainment": ["bookmyshow", "amazon", "flipkart"],
            "gifts": ["amazon", "flipkart", "myntra", "meesho"],
            "photography": ["google", "amazon", "flipkart"],
            "music": ["amazon", "flipkart", "bookmyshow"],
            "games": ["amazon", "flipkart"],
            "accessories": ["amazon", "flipkart", "myntra", "meesho"],
            "transportation": ["makemytrip", "google"],
            "return_gifts": ["amazon", "flipkart", "myntra", "meesho"],
        }
        default_platforms = ["amazon", "flipkart", "google"]

        platform_url_builders = {
            "amazon": lambda q: f"https://www.amazon.in/s?k={urllib.parse.quote_plus(q)}",
            "flipkart": lambda q: f"https://www.flipkart.com/search?q={urllib.parse.quote_plus(q)}",
            "bigbasket": lambda q: f"https://www.bigbasket.com/ps/?q={urllib.parse.quote_plus(q)}",
            "swiggy": lambda q: f"https://www.swiggy.com/search?query={urllib.parse.quote_plus(q)}",
            "zomato": lambda q: f"https://www.zomato.com/search?q={urllib.parse.quote_plus(q)}",
            "bookmyshow": lambda q: f"https://in.bookmyshow.com/search?q={urllib.parse.quote_plus(q)}",
            "myntra": lambda q: f"https://www.myntra.com/search?q={urllib.parse.quote_plus(q)}",
            "meesho": lambda q: f"https://www.meesho.com/search?q={urllib.parse.quote_plus(q)}",
            "google": lambda q: f"https://www.google.com/search?q={urllib.parse.quote_plus(q)}",
            "booking": lambda q: f"https://www.booking.com/search.html?ss={urllib.parse.quote_plus(q)}",
            "makemytrip": lambda q: f"https://www.makemytrip.com/hotels/hotel-listing/?searchText={urllib.parse.quote_plus(q)}",
            "oyorooms": lambda q: f"https://www.oyorooms.com/search/?location={urllib.parse.quote_plus(q)}",
            "nobroker": lambda q: f"https://www.nobroker.in/property/search?searchTerm={urllib.parse.quote_plus(q)}",
        }

        for category in result.get("budget_breakdown", []):
            cat_name = category.get("category", "").lower()
            relevant_platforms = category_platforms.get(cat_name, default_platforms)

            for item in category.get("items", []):
                search_terms = item.get("search_terms", "")
                if search_terms:
                    item["shopping_links"] = {
                        p: platform_url_builders[p](search_terms)
                        for p in relevant_platforms
                        if p in platform_url_builders
                    }

        # ---- Search links for venue suggestions ----
        venue_platforms = ["google", "booking", "makemytrip", "oyorooms", "nobroker"]
        for venue in result.get("venue_suggestions", []):
            search_terms = venue.get("search_terms", "")
            if search_terms:
                venue["search_links"] = {
                    p: platform_url_builders[p](search_terms) for p in venue_platforms
                }

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error generating recommendations: {str(e)}")


# ---------- 3. Jewelry Planner ----------

def get_jewelry_recommendations(budget_input: JewelryBudgetInput, image_path: Optional[str] = None) -> dict:
    """Generate jewelry recommendations based on uploaded dress and budget in INR (India-specific)"""
    try:
        base_prompt = f"""
I need jewelry recommendations for India with a total budget of ₹{budget_input.total_budget:.2f}.

Occasion: {budget_input.occasion}
Preferences: {budget_input.preferences or "Not specified"}
Provide only India-relevant styles, availability, and price ranges in INR.
"""

        json_schema = """
Respond with ONLY valid JSON (no markdown fences) in exactly this structure:
{
    "outfit_analysis": {
        "colors": [],
        "style": "",
        "formality": ""
    },
    "total_budget": 0.0,
    "jewelry_recommendations": [
        {
            "item_type": "",
            "description": "",
            "style": "",
            "estimated_price": 0.0,
            "search_terms": ""
        }
    ],
    "remaining_budget": 0.0,
    "additional_suggestions": []
}
"""

        if image_path:
            # Multimodal call: text + image
            img = Image.open(image_path)
            prompt = (
                base_prompt
                + "\nAn image of the outfit is uploaded. Suggest jewelry that complements it, "
                  "considering color, design, and occasion appropriateness.\n"
                + json_schema
            )
            response = model.generate_content([prompt, img])
        else:
            prompt = base_prompt + "\nNo outfit image was provided; base suggestions on occasion and preferences only.\n" + json_schema
            response = model.generate_content(prompt)

        result = extract_json_from_response(response.text)

        # Add shopping links for each item (India-specific jewelry platforms)
        for item in result.get("jewelry_recommendations", []):
            search_terms = item.get("search_terms", "")
            if search_terms:
                item["shopping_links"] = {
                    "amazon": f"https://www.amazon.in/s?k={urllib.parse.quote_plus(search_terms)}",
                    "flipkart": f"https://www.flipkart.com/search?q={urllib.parse.quote_plus(search_terms)}",
                    "bluestone": f"https://www.bluestone.com/search.html?query={urllib.parse.quote_plus(search_terms)}",
                    "tanishq": f"https://www.tanishq.co.in/search?q={urllib.parse.quote_plus(search_terms)}",
                    "caratlane": f"https://www.caratlane.com/search?q={urllib.parse.quote_plus(search_terms)}",
                    "melorra": f"https://www.melorra.com/search?q={urllib.parse.quote_plus(search_terms)}",
                    "meesho": f"https://www.meesho.com/search?q={urllib.parse.quote_plus(search_terms)}",
                }

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error generating recommendations: {str(e)}")
