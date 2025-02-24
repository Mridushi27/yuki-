"""
Configuration settings for the medical chatbot application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")  # Default to GPT-4 if not specified
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# API Configuration
OPENAI_API_BASE = "https://api.openai.com/v1"
MEDPALM_API_BASE = "https://api.google.com/v1/medpalm"  # Example URL
BIOGPT_API_BASE = "https://api.microsoft.com/v1/biogpt"  # Example URL

# Model Configuration
AVAILABLE_MODELS = {
    "gpt-4": {
        "api_base": OPENAI_API_BASE,
        "max_tokens": 2048,
        "temperature": 0.7,
    },
    "medpalm-2": {
        "api_base": MEDPALM_API_BASE,
        "max_tokens": 1024,
        "temperature": 0.5,
    },
    "biogpt": {
        "api_base": BIOGPT_API_BASE,
        "max_tokens": 1024,
        "temperature": 0.5,
    }
}

# Health Data Configuration
HEALTH_METRICS = {
    "blood_pressure": {
        "systolic_range": (90, 180),
        "diastolic_range": (60, 120)
    },
    "blood_glucose": {
        "range": (70, 200),
        "unit": "mg/dL"
    },
    "heart_rate": {
        "range": (60, 100),
        "unit": "bpm"
    }
}

# Risk Thresholds
RISK_THRESHOLDS = {
    "diabetes": {
        "high": 0.7,
        "medium": 0.4,
        "low": 0.2
    },
    "hypertension": {
        "high": 0.75,
        "medium": 0.5,
        "low": 0.25
    }
}

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
