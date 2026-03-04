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
disease_map = {
    ("chest pain", "difficulty breathing"): "Possible Cardiac Condition",
    ("fever", "cough"): "Possible Viral Infection",
    ("headache", "vomiting"): "Possible Migraine"
}