from fastapi import FastAPI
from schemas.request_schema import SymptomRequest
from schemas.response_schema import SymptomResponse
from models.disease_classifier import classify_disease
from engines.risk_engine import calculate_risk
from engines.recommendation_engine import (
    get_classification,
    get_recommendation
)
from services.translation_service import (
    translate_to_english,
    translate_from_english
)
from services.database_service import save_log

app = FastAPI(title="AI Early Risk Detection & Triage System")


@app.post("/analyze", response_model=SymptomResponse)
def analyze(request: SymptomRequest):

    original_text = request.text

    # Translation
    processed_text = translate_to_english(original_text)

    # Disease classification
    disease_result = classify_disease(processed_text)

    # Risk scoring
    risk_score, contributors = calculate_risk(
        processed_text,
        disease_result["confidence"]
    )

    classification = get_classification(risk_score)
    recommendation = get_recommendation(classification)

    # Save to DB
    save_log({
        "input": original_text,
        "processed": processed_text,
        "risk_score": risk_score,
        "classification": classification,
        "recommendation": recommendation,
        "predicted_condition": disease_result["predicted_condition"],
        "confidence": disease_result["confidence"]
    })

    return SymptomResponse(
        risk_score=risk_score,
        classification=classification,
        recommendation=recommendation,
        predicted_condition=disease_result["predicted_condition"],
        confidence=disease_result["confidence"],
        contributors=contributors,
        disclaimer="This system is for early risk screening only and not a medical diagnosis."
    )