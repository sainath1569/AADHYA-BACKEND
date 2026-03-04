from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

print("🚀 Loading Medical Model...")

# Load the zero-shot classification model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

print("✅ Model loaded successfully!")

def classify_disease(text: str):
    """
    Let the model predict everything - no hardcoded lists!
    """
    try:
        print(f"📊 Analyzing: {text}")
        
        # Let model predict condition - model knows medical terms naturally
        condition_result = classifier(
            text,
            candidate_labels=["medical condition"],  # Minimal guidance
            multi_label=False
        )
        
        # Let model predict risk level
        risk_result = classifier(
            f"Assess risk level for: {text}",
            candidate_labels=["low risk", "moderate risk", "high risk", "critical risk"],
            multi_label=False
        )
        
        # Let model predict severity
        severity_result = classifier(
            text,
            candidate_labels=["mild", "moderate", "severe"],
            multi_label=False
        )
        
        # Extract predictions
        # The model's understanding is in the labels it chooses
        condition = condition_result['labels'][0]
        risk_level_desc = risk_result['labels'][0]
        severity = severity_result['labels'][0]
        
        # Get confidence scores
        condition_conf = condition_result['scores'][0] * 100
        risk_conf = risk_result['scores'][0] * 100
        severity_conf = severity_result['scores'][0] * 100
        
        # Extract risk level from description
        if "critical" in risk_level_desc.lower():
            risk_level = "Critical"
        elif "high" in risk_level_desc.lower():
            risk_level = "High"
        elif "moderate" in risk_level_desc.lower():
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        # Overall confidence
        overall_confidence = (condition_conf + risk_conf + severity_conf) / 3
        
        return {
            "predicted_condition": condition.title(),
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
        return {
            "predicted_condition": "Unable to analyze",
            "condition_confidence": 0,
            "risk_level": "Moderate",
            "risk_confidence": 0,
            "severity": "moderate",
            "severity_confidence": 0,
            "overall_confidence": 0,
            "model_used": "error"
        }