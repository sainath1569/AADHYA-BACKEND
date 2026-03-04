from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Auth Routes
from routes.auth_routes import router as auth_router

# Schemas
from schemas.request_schema import SymptomRequest
from schemas.response_schema import SymptomResponse

# AI Modules
from models.disease_classifier import classify_disease
from engines.risk_engine import calculate_risk
from services.explaination_service import generate_explanation, generate_patient_education
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

# Services
# from services.translation_service import translate_to_english
from services.database_service import save_log

# Utils

# -------------------------------
# CORS (React Frontend)
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include Auth Routes
# -------------------------------

app.include_router(auth_router)

# -------------------------------
# Root Endpoint
# -------------------------------

@app.get("/")
def root():
    return {"message": "Arogya Raksha API Running"}


# -------------------------------
# Symptom Analysis API
# -------------------------------



    try:

        original_text = request.text

        # Parse symptoms, age, gender
        parsed = parse_symptoms_input(original_text)

        symptoms_text = parsed.get("symptoms", "")
        age = parsed.get("age")
        gender = parsed.get("gender")

        print(f"📝 Parsed - Symptoms: {symptoms_text}, Age: {age}, Gender: {gender}")

        # Translate to English
        processed_text = translate_to_english(symptoms_text)

        # Disease Classification
        disease_result = classify_disease(processed_text)

        if not disease_result:
            raise HTTPException(status_code=500, detail="Disease classification failed")

        disease_result["age"] = age
        disease_result["gender"] = gender

        # Risk Calculation
        risk_score, contributors = calculate_risk(
            processed_text,
            disease_result
        )

        contributors = contributors or []

        # Risk Category
        classification = get_classification(risk_score)

        # Recommendation
        recommendation = get_recommendation(classification)

        predicted_condition = disease_result.get("predicted_condition", "Unknown")
        confidence = disease_result.get("overall_confidence", 50)

        # Save Log
        save_log({
            "input": original_text,
            "processed": processed_text,
            "age": age,
            "gender": gender,
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
            disclaimer="This system is for early risk screening only and not a medical diagnosis."
        )

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
