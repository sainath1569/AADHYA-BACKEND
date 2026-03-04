from transformers import pipeline
import warnings
import re
warnings.filterwarnings("ignore")

print("🚀 Loading Advanced Medical Model...")

# Use a more powerful model for comprehensive analysis
# This model can understand context better
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"  # Better for understanding medical context
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

def extract_demographics(text):
    """Extract age and gender from text"""
    age = None
    gender = None
    clean_text = text
    
    # Extract age
    age_patterns = [
        r'age\s+(\d{1,3})',
        r'aged\s+(\d{1,3})',
        r'(\d{1,3})\s*years?',
        r'\b(\d{1,3})\b(?=\s*(?:male|female|man|woman))'
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, text.lower())
        if match:
            age = int(match.group(1))
            clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
            break
    
    # Extract gender
    if re.search(r'\b(male|man|boy|mr)\b', text.lower()):
        gender = "male"
        clean_text = re.sub(r'\b(male|man|boy|mr)\b', '', clean_text, flags=re.IGNORECASE)
    elif re.search(r'\b(female|woman|girl|ms|mrs)\b', text.lower()):
        gender = "female"
        clean_text = re.sub(r'\b(female|woman|girl|ms|mrs)\b', '', clean_text, flags=re.IGNORECASE)
    
    return clean_text.strip(), age, gender

def analyze_with_model(text, candidate_labels):
    """Get model predictions with confidence"""
    result = classifier(text, candidate_labels, multi_label=False)
    return result['labels'][0], result['scores'][0] * 100

def classify_disease(text: str):
    try:
        # Step 1: Extract demographics
        clean_text, age, gender = extract_demographics(text)
        
        # Step 2: Create enhanced text with context
        enhanced_text = clean_text
        if age and gender:
            enhanced_text = f"{clean_text} in a {age}-year-old {gender} patient"
        elif age:
            enhanced_text = f"{clean_text} in a {age}-year-old patient"
        elif gender:
            enhanced_text = f"{clean_text} in a {gender} patient"
        
        print(f"📊 Analyzing: {enhanced_text}")
        
        # Step 3: Let model predict the medical condition
        condition, condition_conf = analyze_with_model(enhanced_text, CONDITIONS)
        
        # Step 4: Let model predict the risk level
        risk_text = f"Symptoms: {enhanced_text}"
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
        
        # Step 5: Let model assess severity
        severity_labels = ["mild symptoms", "moderate symptoms", "severe symptoms"]
        severity, severity_conf = analyze_with_model(enhanced_text, severity_labels)
        
        # Step 6: Combine confidences for overall confidence
        overall_confidence = (condition_conf + risk_conf + severity_conf) / 3
        
        return {
            "predicted_condition": condition,
            "condition_confidence": round(condition_conf, 2),
            "risk_level": risk_level,
            "risk_confidence": round(risk_conf, 2),
            "severity": severity,
            "severity_confidence": round(severity_conf, 2),
            "overall_confidence": round(overall_confidence, 2),
            "age": age,
            "gender": gender,
            "model_used": "facebook/bart-large-mnli"
        }
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return fallback_classification(text)

def fallback_classification(text: str):
    """Enhanced fallback with more intelligence"""
    text_lower = text.lower()
    
    # Simple keyword-based fallback
    if "chest pain" in text_lower:
        return {
            "predicted_condition": "Possible Cardiac Issue",
            "condition_confidence": 70.0,
            "risk_level": "High",
            "risk_confidence": 65.0,
            "severity": "severe symptoms",
            "severity_confidence": 60.0,
            "overall_confidence": 65.0,
            "model_used": "fallback-rule-based"
        }
    elif "breath" in text_lower:
        return {
            "predicted_condition": "Possible Respiratory Issue",
            "condition_confidence": 70.0,
            "risk_level": "High",
            "risk_confidence": 65.0,
            "severity": "moderate symptoms",
            "severity_confidence": 60.0,
            "overall_confidence": 65.0,
            "model_used": "fallback-rule-based"
        }
    else:
        return {
            "predicted_condition": "General Symptoms",
            "condition_confidence": 50.0,
            "risk_level": "Moderate",
            "risk_confidence": 50.0,
            "severity": "mild symptoms",
            "severity_confidence": 50.0,
            "overall_confidence": 50.0,
            "model_used": "fallback-rule-based"
        }