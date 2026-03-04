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
from utils.parser import parse_symptoms_input  # 👈 NEW IMPORT

app = FastAPI(title="AI Early Risk Detection & Triage System")

@app.post("/analyze", response_model=SymptomResponse)
def analyze(request: SymptomRequest):

    original_text = request.text

    # Parse symptoms, age, and gender from input
    parsed = parse_symptoms_input(original_text)
    symptoms_text = parsed["symptoms"]
    age = parsed["age"]
    gender = parsed["gender"]
    
    print(f"📝 Parsed - Symptoms: {symptoms_text}, Age: {age}, Gender: {gender}")

    # Translation
    processed_text = translate_to_english(symptoms_text)

    # Disease classification
    disease_result = classify_disease(processed_text)
    
    # Add age and gender to disease_result
    disease_result["age"] = age
    disease_result["gender"] = gender

    # Risk scoring
    risk_score, contributors = calculate_risk(
        processed_text,
        disease_result
    )

    classification = get_classification(risk_score)
    recommendation = get_recommendation(classification)

    # Save to DB
    save_log({
        "input": original_text,
        "processed": processed_text,
        "age": age,
        "gender": gender,
        "risk_score": risk_score,
        "classification": classification,
        "recommendation": recommendation,
        "predicted_condition": disease_result.get("predicted_condition", "Unknown"),
        "confidence": disease_result.get("overall_confidence", 50)  # ← FIXED!
    })

    return SymptomResponse(
        risk_score=risk_score,
        classification=classification,
        recommendation=recommendation,
        predicted_condition=disease_result.get("predicted_condition", "Unknown"),
        confidence=disease_result.get("overall_confidence", 50),  # ← FIXED!
        contributors=contributors,
        disclaimer="This system is for early risk screening only and not a medical diagnosis."
    )