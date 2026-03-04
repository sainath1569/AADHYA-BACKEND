from pydantic import BaseModel
from typing import List

class SymptomResponse(BaseModel):
    risk_score: int
    classification: str
    recommendation: str
    predicted_condition: str
    confidence: float
    contributors: List[str]
    disclaimer: str