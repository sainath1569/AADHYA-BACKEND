def get_classification(score: int):
    if score <= 25:
        return "Low"
    elif score <= 50:
        return "Moderate"
    elif score <= 75:
        return "High"
    else:
        return "Critical"


def get_recommendation(classification: str):
    mapping = {
        "Low": "Self-care",
        "Moderate": "Teleconsultation",
        "High": "Hospital visit",
        "Critical": "Emergency"
    }
    return mapping[classification]