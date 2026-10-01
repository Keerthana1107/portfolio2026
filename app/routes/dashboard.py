from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import RecommendationHistory
from ..security import current_user
router=APIRouter()
@router.get("/")
def root(request:Request): return RedirectResponse("/dashboard" if request.session.get("access_token") else "/login",303)
@router.get("/dashboard")
def dashboard(request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db); h=db.query(RecommendationHistory).filter_by(user_id=u.id).order_by(RecommendationHistory.created_at.desc()).limit(6).all()
    return request.app.state.templates.TemplateResponse("dashboard.html",{"request":request,"user":u,"history":h})
@router.get("/planner/{planner}")
def planner(planner:str,request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db)
    if planner not in {"home","party","jewelry"}: raise HTTPException(404,"Planner not found.")
    return request.app.state.templates.TemplateResponse(f"{planner}_planner.html",{"request":request,"user":u})
@router.get("/history")
def history(request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db); h=db.query(RecommendationHistory).filter_by(user_id=u.id).order_by(RecommendationHistory.created_at.desc()).all()
    return request.app.state.templates.TemplateResponse("history.html",{"request":request,"user":u,"history":h})
