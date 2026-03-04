from symptom_data import symptom_weights, severity_keywords
from rapidfuzz import process

def extract_symptoms(user_input):
    detected = []

    for symptom in symptom_weights.keys():
        match = process.extractOne(symptom, [user_input])
        if match and match[1] > 80:
            detected.append(symptom)

    return detected


def detect_severity(user_input):
    for word, factor in severity_keywords.items():
        if word in user_input.lower():
            return factor
    return 1  # default moderate


def calculate_risk(user_input):
    user_input = user_input.lower()
    symptoms = extract_symptoms(user_input)
    severity_factor = detect_severity(user_input)

    total_score = 0
    contributors = []

    for symptom in symptoms:
        weight = symptom_weights[symptom]
        score = weight * severity_factor
        total_score += score
        contributors.append(f"{symptom} (weight {weight})")

    normalized_score = min(int(total_score), 100)

    classification = classify_risk(normalized_score)
    recommendation = recommend_action(classification)

    return {
        "risk_score": normalized_score,
        "classification": classification,
        "recommendation": recommendation,
        "contributors": contributors
    }


def classify_risk(score):
    if score <= 25:
        return "Low"
    elif score <= 50:
        return "Moderate"
    elif score <= 75:
        return "High"
    else:
        return "Critical"


def recommend_action(classification):
    mapping = {
        "Low": "Self-care",
        "Moderate": "Teleconsultation",
        "High": "Hospital visit",
        "Critical": "Emergency"
    }
    return mapping[classification]