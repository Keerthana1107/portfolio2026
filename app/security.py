import base64, hashlib, hmac, os, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from .config import SECRET_KEY
from .models import User

def hash_password(password):
    salt=os.urandom(16)
    digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
    return "scrypt$"+base64.urlsafe_b64encode(salt).decode()+"$"+base64.urlsafe_b64encode(digest).decode()

def verify_password(password, encoded):
    try:
        _,s,d=encoded.split("$",2)
        salt=base64.urlsafe_b64decode(s.encode()); expected=base64.urlsafe_b64decode(d.encode())
        actual=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
        return hmac.compare_digest(actual,expected)
    except Exception: return False

def create_access_token(user_id, minutes=1440):
    now=datetime.now(timezone.utc)
    return jwt.encode({"sub":str(user_id),"iat":now,"exp":now+timedelta(minutes=minutes)},SECRET_KEY,algorithm="HS256")

def user_from_token(token,db):
    try: uid=int(jwt.decode(token,SECRET_KEY,algorithms=["HS256"])["sub"])
    except Exception: raise HTTPException(401,"Invalid or expired token.")
    user=db.get(User,uid)
    if not user: raise HTTPException(401,"User not found.")
    return user

def current_user(request:Request,db:Session):
    token=request.session.get("access_token")
    if not token: raise HTTPException(401,"Login required.")
    return user_from_token(token,db)
