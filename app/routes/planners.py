import json
from fastapi import APIRouter,Depends,File,Form,HTTPException,Request,UploadFile
from sqlalchemy.orm import Session
from ..db import get_db
from ..security import current_user
from ..services.recommendation_service import create
from ..config import ALLOWED_IMAGE_TYPES,MAX_UPLOAD_MB
router=APIRouter()
def json_request(r): return "application/json" in r.headers.get("accept","").lower()
@router.post("/generate-home")
async def home(request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db)
    if "application/json" in request.headers.get("content-type",""):
        d=await request.json()
    else:
        f=await request.form()
        items=[]
        for part in str(f.get("items","lighting:2")).split(","):
            if ":" in part:
                k,v=part.split(":",1)
                try: items.append({"category":k.strip(),"quantity":int(v)})
                except: pass
        d={"budget":float(f.get("budget",0)),"rooms":[x.strip() for x in str(f.get("rooms","")).split(",") if x.strip()],
           "style":str(f.get("style","modern")),"items":items or [{"category":"lighting","quantity":1}],
           "priorities":str(f.get("priorities",""))}
    if d["budget"]<=0 or not d["rooms"]: raise HTTPException(422,"Budget and at least one room are required.")
    result,used,hid=create(db,u.id,"home",d)
    return {"ok":True,"ai_used":used,"history_id":hid,"data":result} if json_request(request) else request.app.state.templates.TemplateResponse("recommendations.html",{"request":request,"result":result,"ai_used":used,"history_id":hid,"user":u})
@router.post("/generate-party")
async def party(request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db)
    if "application/json" in request.headers.get("content-type",""): d=await request.json()
    else:
        f=await request.form()
        d={"budget":float(f.get("budget",0)),"guests":int(f.get("guests",1)),"event_type":str(f.get("event_type","birthday")),
           "venue":str(f.get("venue","Not decided")),"city":str(f.get("city","Chennai")),
           "food_preference":str(f.get("food_preference","mixed")),"priorities":str(f.get("priorities",""))}
    if d["budget"]<=0 or d["guests"]<=0: raise HTTPException(422,"Budget and guests must be positive.")
    result,used,hid=create(db,u.id,"party",d)
    return {"ok":True,"ai_used":used,"history_id":hid,"data":result} if json_request(request) else request.app.state.templates.TemplateResponse("recommendations.html",{"request":request,"result":result,"ai_used":used,"history_id":hid,"user":u})
@router.post("/generate-jewelry")
async def jewelry(request:Request,budget:float=Form(...),occasion:str=Form(...),outfit_color:str=Form("not specified"),outfit_style:str=Form("not specified"),jewelry_style:str=Form("elegant"),notes:str=Form(""),image:UploadFile|None=File(None),db:Session=Depends(get_db)):
    u=current_user(request,db)
    if budget<=0: raise HTTPException(422,"Budget must be positive.")
    raw=None; mime=None
    if image and image.filename:
        if image.content_type not in ALLOWED_IMAGE_TYPES: raise HTTPException(400,"Only JPG, PNG and WEBP images are allowed.")
        raw=await image.read()
        if len(raw)>MAX_UPLOAD_MB*1024*1024: raise HTTPException(413,f"Image must be under {MAX_UPLOAD_MB} MB.")
        mime=image.content_type
    d={"budget":budget,"occasion":occasion,"outfit_color":outfit_color,"outfit_style":outfit_style,"jewelry_style":jewelry_style,"notes":notes,"image_attached":bool(raw)}
    result,used,hid=create(db,u.id,"jewelry",d,raw,mime)
    return {"ok":True,"ai_used":used,"history_id":hid,"data":result} if json_request(request) else request.app.state.templates.TemplateResponse("recommendations.html",{"request":request,"result":result,"ai_used":used,"history_id":hid,"user":u})
@router.get("/recommendations-details/{hid}")
def details(hid:int,request:Request,db:Session=Depends(get_db)):
    u=current_user(request,db); from ..models import RecommendationHistory
    x=db.get(RecommendationHistory,hid)
    if not x or x.user_id!=u.id: raise HTTPException(404,"Recommendation not found.")
    return {"id":x.id,"planner":x.planner,"request":json.loads(x.request_json),"response":json.loads(x.response_json),"created_at":x.created_at.isoformat()}
