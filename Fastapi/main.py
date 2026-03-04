from fastapi import FastAPI
from schemas.request_schema import SymptomRequest
from schemas.response_schema import SymptomResponse
from models.disease_classifier import classify_disease
from engines.risk_engine import calculate_risk
from services.gemini_service import generate_explanation, generate_patient_education
from engines.recommendation_engine import (
    get_classification,
    get_recommendation
)

from services.database_service import save_log

app = FastAPI(title="AI Early Risk Detection & Triage System")
@app.post("/analyze", response_model=SymptomResponse)
def analyze(request: SymptomRequest):

    original_text = request.text
    
    print(f"📝 Input text: {original_text}")

    # Disease classification
    disease_result = classify_disease(original_text)

    # Risk scoring
    risk_score, contributors = calculate_risk(
        original_text,
        disease_result
    )

    classification = get_classification(risk_score)
    recommendation = get_recommendation(classification)
    
    predicted_condition = disease_result.get("predicted_condition", "Unknown")
    confidence = disease_result.get("overall_confidence", 50)
    
    # 👇 NEW: Generate explanation using Gemini
    explanation = generate_explanation(
        symptoms_text=original_text,
        risk_score=risk_score,
        classification=classification,
        recommendation=recommendation,
        predicted_condition=predicted_condition,
        confidence=confidence,
        contributors=contributors
    )
    
    # 👇 NEW: Generate patient education (optional)
    patient_education = None
    if predicted_condition != "Unknown" and "fallback" not in disease_result.get("model_used", ""):
        patient_education = generate_patient_education(predicted_condition)

    # Save to DB
    save_log({
        "input": original_text,
        "risk_score": risk_score,
        "classification": classification,
        "recommendation": recommendation,
        "predicted_condition": predicted_condition,
        "confidence": confidence
    })

    return SymptomResponse(
        risk_score=risk_score,
        classification=classification,
        recommendation=recommendation,
        predicted_condition=predicted_condition,
        confidence=confidence,
        contributors=contributors,
        explanation=explanation,  # 👈 NEW
        patient_education=patient_education,  # 👈 NEW
        disclaimer="This system is for early risk screening only and not a medical diagnosis. Always consult a healthcare professional."
    )