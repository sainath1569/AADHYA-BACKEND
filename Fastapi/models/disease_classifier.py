from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

print("🚀 Loading Advanced Medical Model...")

# Use a more powerful model for comprehensive analysis
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

print("✅ Advanced Model loaded successfully!")

# Medical conditions to predict
CONDITIONS = [
    "Heart Attack / Myocardial Infarction",
    "Angina / Chest Pain",
    "Stroke / Brain Attack",
    "Asthma Attack",
    "Pneumonia",
    "COVID-19",
    "Migraine",
    "Seizure",
    "Appendicitis",
    "Food Poisoning",
    "Dehydration",
    "Anxiety Attack",
    "Allergic Reaction",
    "Diabetes Emergency",
    "Hypertensive Crisis"
]

# Risk levels to predict
RISK_LEVELS = [
    "Low Risk - Can be managed at home",
    "Moderate Risk - Need doctor consultation",
    "High Risk - Need hospital visit",
    "Critical Risk - Emergency required"
]

def analyze_with_model(text, candidate_labels):
    """Get model predictions with confidence"""
    result = classifier(text, candidate_labels, multi_label=False)
    return result['labels'][0], result['scores'][0] * 100

def classify_disease(text: str):
    try:
        print(f"📊 Analyzing: {text}")
        
        # Step 1: Let model predict the medical condition
        condition, condition_conf = analyze_with_model(text, CONDITIONS)
        
        # Step 2: Let model predict the risk level
        risk_text = f"Symptoms: {text}"
        risk_level_desc, risk_conf = analyze_with_model(risk_text, RISK_LEVELS)
        
        # Extract risk level from description
        if "Critical" in risk_level_desc:
            risk_level = "Critical"
        elif "High" in risk_level_desc:
            risk_level = "High"
        elif "Moderate" in risk_level_desc:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        # Step 3: Let model assess severity
        severity_labels = ["mild symptoms", "moderate symptoms", "severe symptoms"]
        severity, severity_conf = analyze_with_model(text, severity_labels)
        
        # Step 4: Combine confidences for overall confidence
        overall_confidence = (condition_conf + risk_conf + severity_conf) / 3
        
        return {
            "predicted_condition": condition,
            "condition_confidence": round(condition_conf, 2),
            "risk_level": risk_level,
            "risk_confidence": round(risk_conf, 2),
            "severity": severity,
            "severity_confidence": round(severity_conf, 2),
            "overall_confidence": round(overall_confidence, 2),
            "model_used": "facebook/bart-large-mnli"
        }
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return fallback_classification(text)

def fallback_classification(text: str):
    """Simple fallback if model fails"""
    text_lower = text.lower()
    
    if "chest pain" in text_lower:
        return {
            "predicted_condition": "Possible Cardiac Issue",
            "condition_confidence": 70.0,
            "risk_level": "High",
            "risk_confidence": 65.0,
            "severity": "severe symptoms",
            "severity_confidence": 60.0,
            "overall_confidence": 65.0,
            "model_used": "fallback"
        }
    elif "breath" in text_lower or "breathing" in text_lower:
        return {
            "predicted_condition": "Possible Respiratory Issue",
            "condition_confidence": 70.0,
            "risk_level": "High",
            "risk_confidence": 65.0,
            "severity": "moderate symptoms",
            "severity_confidence": 60.0,
            "overall_confidence": 65.0,
            "model_used": "fallback"
        }
    elif "fever" in text_lower:
        return {
            "predicted_condition": "Possible Infection",
            "condition_confidence": 65.0,
            "risk_level": "Moderate",
            "risk_confidence": 60.0,
            "severity": "moderate symptoms",
            "severity_confidence": 55.0,
            "overall_confidence": 60.0,
            "model_used": "fallback"
        }
    else:
        return {
            "predicted_condition": "General Symptoms",
            "condition_confidence": 50.0,
            "risk_level": "Low",
            "risk_confidence": 50.0,
            "severity": "mild symptoms",
            "severity_confidence": 50.0,
            "overall_confidence": 50.0,
            "model_used": "fallback"
        }