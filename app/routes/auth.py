from fastapi import APIRouter,Depends,Form,Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..security import hash_password,verify_password,create_access_token,user_from_token
router=APIRouter()
@router.get("/register")
def page(request:Request): return request.app.state.templates.TemplateResponse("register.html",{"request":request})
@router.post("/register")
def register(name:str=Form(...),email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    email=email.strip().lower()
    if db.query(User).filter_by(email=email).first(): return RedirectResponse("/register?error=Email+already+registered",303)
    u=User(name=name.strip(),email=email,password_hash=hash_password(password)); db.add(u); db.commit()
    return RedirectResponse("/login?success=Account+created",303)
@router.get("/login")
def login_page(request:Request): return request.app.state.templates.TemplateResponse("login.html",{"request":request})
@router.post("/login")
def login(request:Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=email.strip().lower()).first()
    if not u or not verify_password(password,u.password_hash): return RedirectResponse("/login?error=Invalid+email+or+password",303)
    request.session["access_token"]=create_access_token(u.id); return RedirectResponse("/dashboard",303)
@router.get("/logout")
def logout(request:Request): request.session.clear(); return RedirectResponse("/login?success=Logged+out",303)
@router.post("/api/register")
def api_register(payload:dict,db:Session=Depends(get_db)):
    email=str(payload.get("email","")).strip().lower()
    if db.query(User).filter_by(email=email).first(): return {"ok":False,"error":"Email already registered"}
    u=User(name=str(payload.get("name","")).strip(),email=email,password_hash=hash_password(str(payload.get("password",""))))
    db.add(u); db.commit(); db.refresh(u); return {"ok":True,"user_id":u.id}
@router.post("/token")
def token(request:Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=email.strip().lower()).first()
    if not u or not verify_password(password,u.password_hash): return {"error":"Invalid credentials"}
    t=create_access_token(u.id); request.session["access_token"]=t; return {"access_token":t,"token_type":"bearer"}
@router.get("/session-info")
def session_info(request:Request,db:Session=Depends(get_db)):
    try:
        u=user_from_token(request.session["access_token"],db)
        return {"logged_in":True,"user_id":u.id,"name":u.name,"email":u.email}
    except Exception: return {"logged_in":False}
@router.get("/session-data")
def session_data(request:Request,db:Session=Depends(get_db)):
    u=user_from_token(request.session["access_token"],db)
    return {"logged_in":True,"user_id":u.id,"history_count":len(u.recommendations)}
