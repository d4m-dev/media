from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # 🚀 Import thêm StaticFiles
from contextlib import asynccontextmanager
import asyncio
import os

from core.config import settings
from core.database import init_db, db_manager
from core.scheduler import ai_janitor_task

# Import toàn bộ các router
from api import dashboard, websockets, chatbox, social, auth, widgets, projects, ai_admin
from api import audio_engine # 🚀 Import Trạm Audio mới

from middlewares.logger_tracker import LoggerTrackerMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.dynamic_hosting import DynamicHostingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()                   
    db_manager.connect()   
    db_manager.init_social_tables() 
    task = asyncio.create_task(ai_janitor_task())
    yield 
    task.cancel() 
    if db_manager.connection:
        db_manager.connection.close() 

app = FastAPI(title="Ubuntu Backend Core", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.add_middleware(DynamicHostingMiddleware)
app.add_middleware(LoggerTrackerMiddleware)  
app.add_middleware(RateLimitMiddleware)      

# Đăng ký Routers
app.include_router(auth.router)        
app.include_router(dashboard.router)   
app.include_router(websockets.router)  
app.include_router(chatbox.router)     
app.include_router(social.router)      
app.include_router(widgets.router)     
app.include_router(projects.router)    
app.include_router(ai_admin.router)    
app.include_router(audio_engine.router) # 🚀 Gắn Trạm Audio vào máy chủ

# 🚀 Gắn thư mục tĩnh để tải file Audio về (CDN ảo)
os.makedirs("/storage/emulated/0/coder/media/ubuntu-backend-core/audio_workspace/outputs", exist_ok=True)
app.mount("/audio-files", StaticFiles(directory="/storage/emulated/0/coder/media/ubuntu-backend-core/audio_workspace/outputs"), name="audio_files")

@app.get("/")
async def root(request: Request):
    if "text/html" in request.headers.get("accept", ""):
        hub_path = "/storage/emulated/0/coder/media/ubuntu-backend-core/public/hub.html"
        if os.path.exists(hub_path):
            return FileResponse(hub_path)
    return {"status": "online", "message": "✅ Backend Core đang hoạt động trên Port 16868!"}