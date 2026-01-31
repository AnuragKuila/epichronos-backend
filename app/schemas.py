from pydantic import BaseModel, Field
from typing import Optional


class PatientInfo(BaseModel):
    age: int = Field(..., ge=18, le=90)
    sex: str
    smoking: bool


class Biomarkers(BaseModel):
    RASSF1A_pct: Optional[float] = None
    SEPT9_pct: Optional[float] = None
    APC_pct: Optional[float] = None
    SFRP1_pct: Optional[float] = None
    LINE1_pct: Optional[float] = None

    miR21_FC: Optional[float] = None
    miR34a_FC: Optional[float] = None
    miR155_FC: Optional[float] = None
    miR122_FC: Optional[float] = None

    EpiProxy: Optional[float] = None
    G: Optional[float] = None


class AnalysisRequest(BaseModel):
    patient: PatientInfo
    biomarkers: Biomarkers


class AnalysisResult(BaseModel):
    pclf: float
    gscore: float
    fscore: float
    risk_category: str
    tissue_of_origin: Optional[str] = None
