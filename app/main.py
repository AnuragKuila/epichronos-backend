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
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
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


@app.post("/analyze", response_model=AnalysisResult)
def analyze(data: AnalysisRequest):
    """
    Receives validated patient + biomarker data
    and sends it directly to the ML interface.
    """
    result = predict_risk(data)
    return AnalysisResult(**result)
