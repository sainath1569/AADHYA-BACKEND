symptom_weights = {
    "chest pain": 50,
    "difficulty breathing": 50,
    "shortness of breath": 50,
    "fever": 20,
    "vomiting": 15,
    "headache": 10,
    "unconscious": 80,
    "dizziness": 15,
    "abdominal pain": 25,
    "cough": 15
}

severity_keywords = {
    "mild": 0.5,
    "moderate": 1,
    "severe": 1.5
}

def extract_symptoms(text):
    """Extract symptoms from text"""
    detected = []
    text_lower = text.lower()
    
    for symptom in symptom_weights.keys():
        if symptom in text_lower:
            detected.append(symptom)
    
    return detected

def calculate_risk(text: str, model_output: dict):
    # Get ALL predictions from model (now model does most work!)
    risk_level = model_output.get("risk_level", "Moderate")
    overall_confidence = model_output.get("overall_confidence", 50)
    severity = model_output.get("severity", "moderate symptoms")
    age = model_output.get("age")
    gender = model_output.get("gender")
    
    # Base scores from model's risk level (70% weight to model)
    base_scores = {
        "Low": 20,
        "Moderate": 40,
        "High": 70,
        "Critical": 90
    }
    base_score = base_scores.get(risk_level, 40)
    
    # Start with model's base score
    total_score = base_score * 0.7  # 70% weight to model
    
    # Add symptom-based scoring (30% weight to symptoms)
    severity_factor = 1
    for word, factor in severity_keywords.items():
        if word in text.lower() or word in severity.lower():
            severity_factor = factor
            break
    
    contributors = []
    symptom_score = 0
    for symptom, weight in symptom_weights.items():
        if symptom in text.lower():
            symptom_score += weight * severity_factor
            contributors.append(symptom)
    
    # Add symptom contribution (30%)
    total_score += (symptom_score * 0.3)
    
    # Minor age adjustment (model already considered it, but add slight boost)
    if age and age > 60:
        total_score *= 1.1  # 10% boost for elderly
    
    # Add confidence boost from model
    total_score += overall_confidence * 0.1
    
    # Ensure within 0-100
    risk_score = min(int(total_score), 100)
    
    return risk_score, contributors