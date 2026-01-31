from typing import Dict, Any
from app.ml.inference import predict_patient


def predict_risk(data) -> Dict[str, Any]:
    """
    ML interface for EpiChronos

    Input:
        data (AnalysisRequest):
            Validated FastAPI schema object

    Output:
        Backend-safe ML response
    """

    # -----------------------------
    # Flatten schema → ML input
    # -----------------------------
    input_dict = {
        # Methylation
        "RASSF1A_pct": data.biomarkers.RASSF1A_pct,
        "SEPT9_pct": data.biomarkers.SEPT9_pct,
        "APC_pct": data.biomarkers.APC_pct,
        "SFRP1_pct": data.biomarkers.SFRP1_pct,
        "LINE1_pct": data.biomarkers.LINE1_pct,

        # miRNA
        "miR21_FC": data.biomarkers.miR21_FC,
        "miR34a_FC": data.biomarkers.miR34a_FC,
        "miR155_FC": data.biomarkers.miR155_FC,
        "miR122_FC": data.biomarkers.miR122_FC,

        # Epigenetic
        "EpiProxy": data.biomarkers.EpiProxy,
        "G": data.biomarkers.G,

        # Demographic
        "age": data.patient.age
    }

    # -----------------------------
    # Run ML inference
    # -----------------------------
    ml_result = predict_patient(input_dict)

    risk_score = ml_result["risk_score"]
    risk_level = ml_result["risk_level"]

    # -----------------------------
    # Map ML output → API response
    # -----------------------------
    return {
        "pclf": risk_score,
        "gscore": risk_score,   # same score reused for demo clarity
        "fscore": risk_score,
        "risk_category": risk_level,
        "tissue_of_origin": "Undetermined"
    }
