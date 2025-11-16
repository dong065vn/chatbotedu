"""Main FastAPI application"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn

from app.database import get_db, init_db
from app.chatbot import ChatBot
from app.models import User

# Initialize FastAPI app
app = FastAPI(
    title="Chatbot Quản lý Thời gian",
    description="AI Chatbot hỗ trợ quản lý lịch học, lịch thi và tư vấn thời gian học tập",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    timestamp: str

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables"""
    init_db()
    print("✅ Database initialized successfully")
    print("🚀 Chatbot server is running!")
    print("📱 Open http://localhost:8000 in your browser")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chat interface"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body>
                <h1>Chatbot Quản lý Thời gian</h1>
                <p>Frontend is being set up...</p>
                <p>API Documentation: <a href="/docs">/docs</a></p>
            </body>
        </html>
        """

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Process chat message and return response
    """
    try:
        chatbot = ChatBot(db, user_id=message.user_id)
        result = chatbot.process_message(message.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Chatbot Quản lý Thời gian",
        "version": "1.0.0"
    }

@app.get("/api/user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at.isoformat()
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
