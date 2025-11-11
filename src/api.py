# src/api.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from joblib import load
import pandas as pd
import os
import uuid
from typing import List, Optional
from fastapi.responses import FileResponse

MODEL_PATH = "model/champion_pipeline.joblib"
PREDICTIONS_DIR = "artifacts/predictions"

os.makedirs(PREDICTIONS_DIR, exist_ok=True)

app = FastAPI(title="Bank Marketing - Prediction API", version="1.0")

# Allow CORS for local dev (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for single-row input (add fields you expect)
class PredictRequest(BaseModel):
    age: int
    job: Optional[str] = None
    marital: Optional[str] = None
    education: Optional[str] = None
    default: Optional[str] = None
    balance: float
    housing: Optional[str] = None
    loan: Optional[str] = None
    contact: Optional[str] = None
    day: Optional[int] = None
    month: Optional[str] = None
    campaign: Optional[int] = None
    pdays: Optional[int] = None
    previous: Optional[int] = None
    poutcome: Optional[str] = None

# Load model on startup
try:
    model = load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Model load error: {e}")

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=dict)
def predict(payload: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    # convert to DataFrame (single-row)
    X = pd.DataFrame([payload.dict()])
    try:
        proba = model.predict_proba(X)[:, 1][0]
        label = int(proba >= 0.5)
        return {"y_proba": float(proba), "y_pred": label}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...), threshold: float = 0.5):
    """
    Accepts a CSV file, returns a CSV file with predictions saved to artifacts/predictions,
    and returns the download filename reference.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported")

    # read CSV into pandas
    contents = await file.read()
    try:
        df = pd.read_csv(pd.io.common.BytesIO(contents), sep=None, engine="python")
    except Exception:
        # fallback to default comma
        df = pd.read_csv(pd.io.common.BytesIO(contents))

    # perform predictions
    try:
        preds_proba = model.predict_proba(df)[:, 1]
        preds_label = (preds_proba >= threshold).astype(int)
        df_out = df.copy()
        df_out["y_proba"] = preds_proba
        df_out["y_pred"] = preds_label
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

    out_name = f"predictions_{uuid.uuid4().hex[:8]}.csv"
    out_path = os.path.join(PREDICTIONS_DIR, out_name)
    df_out.to_csv(out_path, index=False)

    return {"predictions_file": out_name, "rows": len(df_out)}

@app.get("/predictions/{filename}")
def get_predictions_file(filename: str):
    filepath = os.path.join(PREDICTIONS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="text/csv", filename=filename)

