"""
FastAPI main application for the medical chatbot.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

from .config import API_HOST, API_PORT, DEBUG_MODE
from .utils import logger
from .chatbot import medical_chatbot
from .ml_model import risk_predictor

# Initialize FastAPI app
app = FastAPI(
    title="Medical Chatbot API",
    description="API for medical chatbot with disease risk prediction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class HealthDataRequest(BaseModel):
    blood_glucose: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    heart_rate: Optional[float] = None
    age: Optional[int] = None
    bmi: Optional[float] = None
    medical_history: Optional[List[str]] = None

class ChatResponse(BaseModel):
    response: str
    model_used: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    predictions: Dict[str, Any]
    error: Optional[str] = None

# API Routes
@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"status": "running", "service": "Medical Chatbot API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return the chatbot's response.
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        response = await medical_chatbot.get_response(request.message, request.context)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
            
        return ChatResponse(
            response=response["response"],
            model_used=response["model_used"]
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/health", response_model=HealthResponse)
async def predict_health_risks(request: HealthDataRequest):
    """
    Process health data and return risk predictions.
    """
    try:
        logger.info("Received health data for risk prediction")
        
        # Convert request model to dictionary
        health_data = request.dict()
        
        # Get predictions
        predictions = risk_predictor.predict_risk(health_data)
        
        if "error" in predictions:
            raise HTTPException(status_code=500, detail=predictions["error"])
            
        return HealthResponse(predictions=predictions)
        
    except Exception as e:
        logger.error(f"Error processing health data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health-check")
async def health_check():
    """
    Health check endpoint to verify all components are functioning.
    """
    try:
        # Verify chatbot is working
        test_response = await medical_chatbot.get_response("test", None)
        if "error" in test_response:
            return {
                "status": "error",
                "chatbot": "not responding",
                "ml_model": "unknown"
            }
            
        # Verify ML model is working
        test_prediction = risk_predictor.predict_risk({
            "blood_glucose": 100,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 75,
            "age": 40,
            "bmi": 25
        })
        if "error" in test_prediction:
            return {
                "status": "error",
                "chatbot": "working",
                "ml_model": "not responding"
            }
            
        return {
            "status": "healthy",
            "chatbot": "working",
            "ml_model": "working"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def start():
    """Start the FastAPI server."""
    uvicorn.run(
        "backend.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG_MODE
    )

if __name__ == "__main__":
    start()
