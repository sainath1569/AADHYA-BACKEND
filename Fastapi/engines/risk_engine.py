def extract_symptoms(text):
    """Extract symptoms from text for display purposes only"""
    common_symptoms = [
        "chest pain", "difficulty breathing", "shortness of breath",
        "fever", "vomiting", "headache", "unconscious", "dizziness",
        "abdominal pain", "cough"
    ]
    
    detected = []
    text_lower = text.lower()
    
    for symptom in common_symptoms:
        if symptom in text_lower:
            detected.append(symptom)
    
    return detected

def calculate_risk(text: str, model_output: dict):
    """
    Risk score comes DIRECTLY from the model!
    This function just maps model output to 0-100 scale
    """
    
    # Get model predictions
    risk_level = model_output.get("risk_level", "Moderate")
    severity = model_output.get("severity", "moderate")
    confidence = model_output.get("overall_confidence", 50)
    
    # Base scores from model's risk level
    base_scores = {
        "Low": 20,
        "Moderate": 40,
        "High": 70,
        "Critical": 90
    }
    
    # Start with model's risk level
    risk_score = base_scores.get(risk_level, 40)
    
    # Adjust based on severity (from model)
    if "severe" in severity.lower():
        risk_score += 15
    elif "mild" in severity.lower():
        risk_score -= 10
    
    # Adjust based on model confidence
    risk_score = int(risk_score * (confidence / 100) * 1.2)  # Scale to 0-100
    
    # Ensure within 0-100
    risk_score = max(0, min(100, risk_score))
    
    # Extract symptoms for display (NOT for calculation)
    contributors = extract_symptoms(text)
    
    return risk_score, contributors