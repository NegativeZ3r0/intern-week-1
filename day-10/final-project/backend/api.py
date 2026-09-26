import os
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


class FacilityData(BaseModel):
    cleanliness_score: float = Field(..., ge=0.0, le=10.0)
    odor_score: float = Field(..., ge=0.0, le=10.0)
    waste_level: float = Field(..., ge=0.0, le=100.0)
    complaints: int = Field(..., ge=0)
    footfall: int = Field(..., ge=0)
    hours_since_cleaning: float = Field(..., ge=0.0)

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "ml" / "dataset" / "facility_hygiene_ml_dataset_cleaned.xlsx"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Builds and trains the ML pipeline in memory, yielding it to the application state."""
    # 1. Load Data
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Training dataset not found at: {DATASET_PATH}")

    # 1. Load Data
    df = pd.read_excel(DATASET_PATH)
    features = ['cleanliness_score', 'odor_score', 'waste_level', 'complaints', 'footfall', 'hours_since_cleaning']
    data_cleaned = df.dropna(subset=features + ['hygiene_risk']).copy()

    X = data_cleaned[features]
    y = data_cleaned['hygiene_risk']

    # 2. Encode Labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y.astype(str))

    # 3. Construct and Fit Pipeline
    inference_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', GradientBoostingClassifier(random_state=42, learning_rate=0.2))
    ])
    inference_pipeline.fit(X, y_encoded)

    # Expose the models safely without using global variables
    yield {"pipeline": inference_pipeline, "encoder": label_encoder}

    # Memory cleanup when the server shuts down

# Initialize the ASGI application with the lifespan context manager
app = FastAPI(title="Smart Hygiene Risk Prediction API", lifespan=lifespan)

# Parse a comma-separated string of allowed origins from the environment.
# Fallback to the default Vite local dev server port if the variable is not set.
raw_origins = os.environ.get("FRONTEND_URL", "http://localhost:5173")
origins = [origin.strip() for origin in raw_origins.split(",")]

# Allow Cross-Origin requests from the specified frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict_risk(data: FacilityData, request: Request):
    """Endpoint to receive facility metrics and return the risk classification."""
    # Retrieve the model artifacts from the ASGI state
    pipeline = request.state.pipeline
    encoder = request.state.encoder

    # Deserialization and Forward Pass
    input_df = pd.DataFrame([data.model_dump()])
    prediction_encoded = pipeline.predict(input_df)
    predicted_class = encoder.inverse_transform(prediction_encoded)[0]

    return {
        "status": "success",
        "predicted_hygiene_risk": predicted_class
    }

if __name__ == "__main__":
    # Use environment port for Render compatibility
    port = int(os.environ.get("PORT", '8000'))
    uvicorn.run(app, host="0.0.0.0", port=port)
