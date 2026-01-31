import os
import joblib
import pandas as pd

# -------------------------------------------------
# Path-safe model loading (CRITICAL for FastAPI)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "risk_model.pkl"))
features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))
imputer = joblib.load(os.path.join(MODEL_DIR, "median_imputer.pkl"))

# -------------------------------------------------
# Feature groups
# -------------------------------------------------

methylation_features = [
    "RASSF1A_pct",
    "SEPT9_pct",
    "APC_pct",
    "SFRP1_pct",
    "LINE1_pct"
]

# -------------------------------------------------
# Risk categorization
# -------------------------------------------------


def risk_category(score: float) -> str:
    if score < 0.4:
        return "Low"
    elif score < 0.7:
        return "Moderate"
    else:
        return "High"

# -------------------------------------------------
# Main inference function
# -------------------------------------------------


def predict_patient(input_dict: dict) -> dict:
    """
    input_dict:
        Dictionary with patient + biomarker data.
        Keys must match training feature names.
        Missing values are allowed.
    """

    df = pd.DataFrame([input_dict])

    # Auto-compute tumor_mean if missing
    if "tumor_mean" not in df.columns:
        df["tumor_mean"] = df[methylation_features].mean(axis=1)

    # Ensure all trained features exist
    for col in features:
        if col not in df.columns:
            df[col] = None

    # Apply imputation + prediction
    df[features] = imputer.transform(df[features])
    X = df[features]

    risk_score = model.predict_proba(X)[0, 1]
    risk_level = risk_category(risk_score)

    return {
        "risk_score": float(risk_score),
        "risk_level": risk_level
    }
