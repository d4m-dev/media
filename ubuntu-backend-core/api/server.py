from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from core.telegram import telegram_polling_task
import asyncio
import os

from core.config import settings
from core.database import init_db, db_manager
from core.scheduler import ai_janitor_task

from api import dashboard, websockets, chatbox, social, auth, widgets, projects, ai_admin, audio_engine

from middlewares.logger_tracker import LoggerTrackerMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.dynamic_hosting import DynamicHostingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()                   
    db_manager.connect()   
    db_manager.init_social_tables() 
    task = asyncio.create_task(ai_janitor_task())
    task_telegram = asyncio.create_task(telegram_polling_task())
    yield 
    task.cancel()
    task_telegram.cancel()
    if db_manager.connection:
        db_manager.connection.close() 

app = FastAPI(title="Ubuntu Backend Core", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(DynamicHostingMiddleware)
app.add_middleware(LoggerTrackerMiddleware)  
app.add_middleware(RateLimitMiddleware)      

# Đăng ký các module API
app.include_router(auth.router)        
app.include_router(dashboard.router)   
app.include_router(websockets.router)  
app.include_router(chatbox.router)     
app.include_router(social.router)      
app.include_router(widgets.router)     
app.include_router(projects.router)    
app.include_router(ai_admin.router)    
app.include_router(audio_engine.router)

# ==========================================
# 🚀 TỰ ĐỘNG NHẬN DIỆN ĐƯỜNG DẪN GỐC (DYNAMIC PATH)
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
AUDIO_OUTPUT_DIR = os.path.join(BASE_DIR, "audio_workspace", "outputs")

os.makedirs(os.path.join(PUBLIC_DIR, "js"), exist_ok=True)
app.mount("/js", StaticFiles(directory=os.path.join(PUBLIC_DIR, "js")), name="js")

os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
app.mount("/audio-files", StaticFiles(directory=AUDIO_OUTPUT_DIR), name="audio_files")

# ==========================================
# ĐỊNH TUYẾN FRONTEND
# ==========================================
@app.get("/")
@app.get("/hub.html")
async def serve_hub():
    """Trang chủ mặt tiền: Hub Trưng Bày"""
    hub_path = os.path.join(PUBLIC_DIR, "hub.html")
    if os.path.exists(hub_path):
        return FileResponse(hub_path)
    return {"status": "error", "message": "Không tìm thấy hub.html"}

@app.get("/admin/dashboard")
@app.get("/admin/dashboard/")
async def serve_dashboard():
    """Trang Quản trị (Giấu kín)"""
    index_path = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "error", "message": "Không tìm thấy index.html"}

@app.get("/audio-test.html")
async def serve_audio_test():
    """Trang công cụ Studio"""
    audio_path = os.path.join(PUBLIC_DIR, "audio-test.html")
    if os.path.exists(audio_path):
        return FileResponse(audio_path)
    return {"status": "error", "message": "Không tìm thấy audio-test.html"}