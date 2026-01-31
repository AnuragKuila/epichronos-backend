from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalysisRequest, AnalysisResult
from app.ml_interface import predict_risk

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(
    title="EpiChronos Backend",
    version="1.0.0",
    description="Backend API for cancer risk estimation",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# -----------------------------
# CORS CONFIGURATION
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Routes
# -----------------------------


@app.get("/")
def root():
    """
    Health check endpoint
    """
    return {"status": "EpiChronos backend running"}


@app.post("/analyze")
def analyze(data: Dict[str, Any]):
    result = predict_risk(data)
    return result
