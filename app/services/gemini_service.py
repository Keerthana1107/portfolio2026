import json
from google import genai
from google.genai import types
from ..config import GEMINI_API_KEY,GEMINI_MODEL
from ..catalog import catalog_for,search_url
from .fallback import fallback

class GeminiService:
    def __init__(self):
        self.client=genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
    def generate(self,planner,data,image_bytes=None,mime=None):
        if not self.client: return fallback(planner,data),False
        cat=catalog_for(planner)
        prompt=f"""You are PocketSmart AI, a budget planning assistant.
Planner: {planner}
User data: {json.dumps(data)}
Candidate catalog: {json.dumps(cat)}
Return ONLY valid JSON:
{{"summary":"string","budget_allocation":{{"category":number}},"recommendations":[{{"catalog_index":0,"reason":"string"}}],"tips":["string"]}}
Rules: stay within the total budget; select only catalog indexes supplied; do not invent live prices, stock, ratings, reviews or URLs; give 3-6 useful suggestions."""
        try:
            contents=[prompt]
            if image_bytes and mime:
                contents.insert(0,types.Part.from_bytes(data=image_bytes,mime_type=mime))
            r=self.client.models.generate_content(
                model=GEMINI_MODEL,contents=contents,
                config=types.GenerateContentConfig(temperature=.3,response_mime_type="application/json"))
            obj=json.loads((r.text or "").strip())
            rec=[]
            for x in obj.get("recommendations",[])[:6]:
                i=int(x.get("catalog_index",-1))
                if 0<=i<len(cat):
                    p=cat[i]
                    rec.append({"title":p["name"],"category":p["category"],"platform":p["platform"],
                                "estimated_price":p["price"],"reason":x.get("reason","Selected for your requirements."),
                                "search_url":search_url(p["platform"],p["q"])})
            if not rec: raise ValueError("No valid recommendations")
            obj.update(planner=planner,budget=float(data["budget"]),recommendations=rec,
                       disclaimer="Catalog prices are illustrative; verify current price, availability and seller details.")
            return obj,True
        except Exception:
            return fallback(planner,data),False
