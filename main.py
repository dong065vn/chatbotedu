"""
Main FastAPI Application - Optimized v2.0
Educational Chatbot with Gemini AI Integration
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn
import os
from pathlib import Path

from app.database import get_db, init_db
from app.chatbot_v2 import ChatBotV2
from app.models import User

# Configuration
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    init_db()
    print("✅ Database initialized successfully")
    
    gemini_status = "ENABLED" if os.getenv("GEMINI_API_KEY") else "DISABLED"
    print(f"🤖 Gemini AI: {gemini_status}")
    
    if gemini_status == "DISABLED":
        print("⚠️  Set GEMINI_API_KEY in .env to enable AI features")
    
    print("🚀 Chatbot server is running!")
    print("📱 Open http://localhost:8000 in your browser")
    
    yield
    
    # Shutdown
    print("👋 Shutting down chatbot server...")

# Initialize FastAPI app with optimizations
app = FastAPI(
    title="Chatbot Quản lý Thời gian",
    description="AI Chatbot with Gemini - Smart schedule and study management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files with cache control
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Pydantic models for API
class ChatMessage(BaseModel):
    """Chat message request model"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    user_id: Optional[int] = Field(None, description="User ID (optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Lịch học hôm nay",
                "user_id": 1
            }
        }

class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool = Field(..., description="Request success status")
    response: str = Field(..., description="Bot response message")
    timestamp: str = Field(..., description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "Bạn có 2 lịch học hôm nay...",
                "timestamp": "2024-01-01T10:00:00"
            }
        }

class UserResponse(BaseModel):
    """User information response"""
    id: int
    username: str
    created_at: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    gemini_enabled: bool

# Routes
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root():
    """Serve the main chat interface"""
    index_file = STATIC_DIR / "index.html"
    
    if index_file.exists():
        return FileResponse(index_file)
    
    return HTMLResponse(
        content="""
        <html>
            <head><title>Chatbot Quản lý Thời gian</title></head>
            <body style="font-family: Arial; padding: 40px; text-align: center;">
                <h1>🤖 Chatbot Quản lý Thời gian</h1>
                <p>Frontend is being set up...</p>
                <p><a href="/docs">📚 API Documentation</a></p>
            </body>
        </html>
        """,
        status_code=200
    )

@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Process chat message",
    description="Send a message and receive AI-powered response"
)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Process chat message and return response with Gemini AI
    
    - **message**: User's message text
    - **user_id**: Optional user identifier
    """
    try:
        chatbot = ChatBotV2(db, user_id=message.user_id, use_gemini=True)
        result = chatbot.process_message(message.message)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get(
    "/api/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check service health and status"
)
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Chatbot Quản lý Thời gian",
        "version": "2.0.0",
        "gemini_enabled": bool(os.getenv("GEMINI_API_KEY"))
    }

@app.get(
    "/api/user/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user information",
    description="Retrieve user details by ID"
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user information by user ID
    
    - **user_id**: User identifier
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at.isoformat()
    }

@app.get("/api/stats", summary="Get application statistics")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about schedules, exams, and users"""
    try:
        from app.models import Schedule, Exam
        
        total_users = db.query(User).count()
        total_schedules = db.query(Schedule).count()
        total_exams = db.query(Exam).count()
        
        return {
            "total_users": total_users,
            "total_schedules": total_schedules,
            "total_exams": total_exams
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return HTMLResponse(
        content="""
        <html>
            <head><title>404 - Not Found</title></head>
            <body style="font-family: Arial; padding: 40px; text-align: center;">
                <h1>404 - Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
                <a href="/">← Back to Home</a>
            </body>
        </html>
        """,
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return HTMLResponse(
        content="""
        <html>
            <head><title>500 - Server Error</title></head>
            <body style="font-family: Arial; padding: 40px; text-align: center;">
                <h1>500 - Internal Server Error</h1>
                <p>Something went wrong. Please try again later.</p>
                <a href="/">← Back to Home</a>
            </body>
        </html>
        """,
        status_code=500
    )

# Main entry point
if __name__ == "__main__":
    # Run the application with optimized settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development") == "development",
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
        access_log=True
    )
