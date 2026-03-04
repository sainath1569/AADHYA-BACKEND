from pydantic import BaseModel
from typing import List, Optional

class SymptomResponse(BaseModel):
    risk_score: int
    classification: str
    recommendation: str
    predicted_condition: str
    confidence: float
    contributors: List[str]
    explanation: str  # 👈 NEW: Gemini-generated explanation
    patient_education: Optional[str] = None  # 👈 NEW: Optional education
    disclaimer: str