import requests
import streamlit as st

# Define the FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Hygiene Risk Predictor", layout="centered")

st.title("Smart Hygiene Risk Prediction")
st.write("Enter the facility metrics below to predict the current hygiene risk level.")

# Create a form to gather user inputs cleanly
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        cleanliness_score = st.number_input("Cleanliness Score", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        odor_score = st.number_input("Odor Score", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        waste_level = st.number_input("Waste Level", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

    with col2:
        complaints = st.number_input("Complaints", min_value=0, value=0, step=1)
        footfall = st.number_input("Footfall", min_value=0, value=100, step=10)
        hours_since_cleaning = st.number_input("Hours Since Cleaning", min_value=0.0, value=2.0, step=0.5)

    # Submit button
    submitted = st.form_submit_button("Predict Risk")

if submitted:
    # 1. Serialize inputs into a dictionary matching the FastAPI schema
    payload = {
        "cleanliness_score": cleanliness_score,
        "odor_score": odor_score,
        "waste_level": waste_level,
        "complaints": complaints,
        "footfall": footfall,
        "hours_since_cleaning": hours_since_cleaning
    }

    # 2. Transmit the data to the API and handle the response
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        risk_level = result.get("predicted_hygiene_risk", "Unknown")

        # Display the result with dynamic color coding
        if risk_level == "High":
            st.error(f"**Predicted Hygiene Risk:** {risk_level}")
        elif risk_level == "Medium":
            st.warning(f"**Predicted Hygiene Risk:** {risk_level}")
        else:
            st.success(f"**Predicted Hygiene Risk:** {risk_level}")

    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Is the FastAPI server running on http://127.0.0.1:8000?")
