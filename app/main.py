from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .config import BASE_DIR,APP_NAME,SECRET_KEY,SESSION_COOKIE
from .db import Base,engine
from .routes import auth,planners,dashboard
Base.metadata.create_all(bind=engine)
app=FastAPI(title=APP_NAME,version="1.0.0")
app.add_middleware(SessionMiddleware,secret_key=SECRET_KEY,session_cookie=SESSION_COOKIE,same_site="lax",https_only=False)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.state.templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
app.mount("/static",StaticFiles(directory=str(BASE_DIR/"static")),name="static")
app.include_router(auth.router); app.include_router(planners.router); app.include_router(dashboard.router)
@app.get("/health")
def health(): return {"status":"ok","app":APP_NAME}
@app.get("/startup")
def startup(): return {"status":"ready"}
if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
