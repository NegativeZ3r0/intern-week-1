# Smart Hygiene Risk Prediction System

## Project Overview
This project is an end-to-end machine learning system designed to predict facility hygiene risk levels (Low, Medium, High). From an implementation perspective, it is structured as a decoupled microservice architecture consisting of a modular data preprocessing/training pipeline, a FastAPI REST backend for inference, and a Streamlit frontend client.

## Problem Statement
Facilities currently rely on reactive, manual inspections to manage cleanliness. The goal is to build a proactive, data-driven classification model that maps continuous operational metrics (such as footfall, waste levels, and hours since last cleaning) to discrete risk categories, allowing for optimized resource allocation and automated cleaning schedules.

## Technology Stack
* **Data Processing & Modeling:** Python, Pandas, Scikit-learn (Pipeline, StandardScaler, Gradient Boosting, Random Forest)
* **Backend / API:** FastAPI, Uvicorn, Pydantic (for strictly typed JSON deserialization)
* **Frontend:** Streamlit, Requests

## Architecture
The system follows a strict separation of concerns to ensure scalability:
1. **Training Pipeline:** Modular scripts (`eda.py`, `preprocess.py`, `train.py`, `evaluate.py`) orchestrated by `main.py` generate statistical insights and evaluate model performance locally.
2. **Inference Server (`api.py`):** Wraps the data scaler and classifier into a single `sklearn.pipeline.Pipeline` loaded into ASGI application memory via a lifespan context manager.
3. **Presentation Tier (`ui.py`):** A stateless Streamlit application that manages UI validation, serializes user inputs, and communicates with the backend via HTTP REST calls.

## API Documentation
**Endpoint:** `POST /predict`  
**Description:** Accepts facility metrics and returns the predicted risk classification.

**Request Body Schema (JSON):**
* `cleanliness_score` (float): `0.0` to `10.0`
* `odor_score` (float): `0.0` to `10.0`
* `waste_level` (float): `0.0` to `100.0`
* `complaints` (integer): `>= 0`
* `footfall` (integer): `>= 0`
* `hours_since_cleaning` (float): `>= 0.0`

**Success Response (200 OK):**
```json
{
  "status": "success",
  "predicted_hygiene_risk": "High"
}
```

**Validation Error Response (422 Unprocessable Entity):** Returned automatically if values exceed defined ranges.

## Installation

1. Clone the repository and set up an isolated virtual environment.
*Reason:* This prevents dependency conflicts with system-level Python packages.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```


2. Install the required dependencies:
make sure your present working directory is `intern-week-1/day-10/`
```bash
pip install -r requirements.txt
```



## How to Run

Because the backend and frontend run on separate servers, they must be executed in separate terminal instances.

**1. Start the API Server:**
make sure your present working directory is `intern-week-1/day-10/ml/`

```bash
uvicorn api:app --reload
```

*Reason:* This initializes the FastAPI application, trains the pipeline in memory during startup, and binds it to `127.0.0.1:8000`.

**2. Start the Frontend UI:**
make sure your present working directory is `intern-week-1/day-10/streamlit_ui/`
Open a new terminal window, ensure your virtual environment is activated, and run:

```bash
streamlit run ui.py
```

*Reason:* This launches the client interface locally (typically on port `8501`), which will securely route user inputs to your active API.

## Challenges Faced

* **Type Safety & State Management:** Storing the trained model as a global variable initially caused static type-checking errors (e.g., calling `.predict()` on variables initialized as `None`).
* **Data Leakage during Inference:** Applying standard scaling to individual, single-row API requests independently can warp the feature distribution if not tied to the training dataset's exact mathematical baseline.
* **Data Integrity:** Relying solely on client-side Streamlit UI constraints for value ranges (e.g., waste level capping at 100) left the ML model exposed to invalid or malicious inputs if the API was pinged directly via `curl` or Postman.

## Solutions

* **Modernized ASGI State:** Implemented FastAPI's `@asynccontextmanager` to yield the trained pipeline directly into the application's `request.state`. *Reason:* This cleanly manages memory allocation and satisfies strict static analysis tools by eliminating global `None` states.
* **Bundled Pipelines:** Wrapped `StandardScaler` and `GradientBoostingClassifier` into an `sklearn.pipeline.Pipeline`. *Reason:* This forces the inference engine to automatically transform incoming JSON payloads using the exact statistical mean and variance parameters learned during the initial training phase.
* **Dual-Layer Validation:** Enforced strict mathematical boundaries using Pydantic `Field` validators at the API schema level. *Reason:* This intercepts and rejects out-of-bounds HTTP requests before they reach the model pipeline, guaranteeing inference integrity.

## Future Improvements

* **Hyperparameter Tuning:** Implement `GridSearchCV` to optimize the Gradient Boosting parameters (learning rate, max depth). *Reason:* This will help better separate the complex boundary edge cases currently causing slight class confusion in "Medium Risk" predictions.
* **Containerization:** Wrap both the FastAPI backend and Streamlit frontend using Docker and `docker-compose`. *Reason:* This ensures environmental parity, making the application instantly deployable on cloud infrastructure without resolving manual dependency trees.
