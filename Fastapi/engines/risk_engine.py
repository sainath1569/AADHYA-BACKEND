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

def calculate_risk(text: str, disease_confidence: float):
    text = text.lower()
    total_score = 0
    contributors = []

    severity_factor = 1
    for word, factor in severity_keywords.items():
        if word in text:
            severity_factor = factor
            break

    for symptom, weight in symptom_weights.items():
        if symptom in text:
            score = weight * severity_factor
            total_score += score
            contributors.append(symptom)

    # Add disease confidence boost
    total_score += disease_confidence * 0.2

    risk_score = min(int(total_score), 100)

    return risk_score, contributors