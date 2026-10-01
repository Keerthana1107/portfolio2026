import json
from ..models import RecommendationHistory
from .gemini_service import GeminiService
ai=GeminiService()
def create(db,user_id,planner,data,image=None,mime=None):
    result,used=ai.generate(planner,data,image,mime)
    row=RecommendationHistory(user_id=user_id,planner=planner,request_json=json.dumps(data),response_json=json.dumps(result))
    db.add(row); db.commit(); db.refresh(row)
    return result,used,row.id
