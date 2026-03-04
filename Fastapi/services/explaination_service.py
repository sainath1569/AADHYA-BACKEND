import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# Configure Gemini
GEMINI_API_KEY = "AIzaSyB0DWK9hwiP4WzZuJABcYjxxMhxBlGUmkA"
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest model
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_explanation(symptoms_text, risk_score, classification, recommendation, predicted_condition, confidence, contributors):
    """
    Generate a brief, helpful explanation using Gemini API
    """
    try:
        prompt = f"""
        You are a medical triage assistant. Provide a brief, clear explanation (max 3 sentences) for this patient:
        
        Symptoms: {symptoms_text}
        Detected symptoms: {', '.join(contributors)}
        Risk Score: {risk_score}/100 ({classification})
        Recommendation: {recommendation}
        Predicted Condition: {predicted_condition} (Confidence: {confidence}%)
        
        Write a compassionate, informative explanation that:
        1. Acknowledges their symptoms
        2. Explains why we gave this risk level
        3. Reiterates the recommended action
        4. Includes disclaimer
        
        Keep it very concise - max 3 sentences.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return fallback_explanation(symptoms_text, risk_score, classification, recommendation, predicted_condition, confidence, contributors)

def fallback_explanation(symptoms_text, risk_score, classification, recommendation, predicted_condition, confidence, contributors):
    """Simple fallback if Gemini API fails"""
    
    explanations = {
        "Critical": f"⚠️ Your symptoms ({', '.join(contributors)}) indicate a {classification.lower()} risk condition - {predicted_condition}. This requires IMMEDIATE emergency care. Please call emergency services or go to the nearest hospital right away.",
        
        "High": f"🫁 Based on your symptoms ({', '.join(contributors)}), we've identified a {classification.lower()} risk of {predicted_condition}. You should visit a hospital for proper evaluation within the next few hours.",
        
        "Moderate": f"💊 Your symptoms ({', '.join(contributors)}) suggest a {classification.lower()} risk condition - possibly {predicted_condition}. Please consult with a doctor via teleconsultation or visit a clinic today.",
        
        "Low": f"😊 Your symptoms ({', '.join(contributors)}) appear to be {classification.lower()} risk. You can manage this with self-care at home. If symptoms worsen, consult a doctor."
    }
    
    return explanations.get(classification, f"Based on your symptoms, we recommend {recommendation.lower()}.")

def generate_patient_education(condition):
    """
    Generate brief patient education for the predicted condition
    """
    try:
        prompt = f"""
        Provide ONE brief sentence of patient education for someone diagnosed with {condition}.
        Focus on what they should know or do. Keep it to 15 words max.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Gemini education error: {e}")
        return f"Follow your doctor's advice for managing {condition}."