from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import lightgbm as lgb
import numpy as np
import pandas as pd
import os
from typing import List

app = FastAPI(title="Credit Card Fraud Detection API")

# Model path
MODEL_PATH = "src/model.txt"
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = lgb.Booster(model_file=MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print("Model file not found. Make sure to run training first.")

class Transaction(BaseModel):
    # Expecting 28 PCA features (V1-V28) and Amount
    features: List[float] # V1...V28, Amount (29 features)

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running"}

@app.post("/predict")
def predict(transaction: Transaction):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(transaction.features) != 29:
        raise HTTPException(status_code=400, detail="Expected 29 numerical features (V1-V28, Amount)")
    
    # Preprocess and predict
    features_array = np.array(transaction.features).reshape(1, -1)
    prediction_prob = model.predict(features_array)[0]
    
    is_fraud = bool(prediction_prob > 0.5)
    
    return {
        "is_fraud": is_fraud,
        "fraud_probability": float(prediction_prob)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
