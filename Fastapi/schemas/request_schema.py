from pydantic import BaseModel
from typing import Optional

class SymptomRequest(BaseModel):
    text: str  # This will contain everything: symptoms + age + gender
    language: str = "en"
    # Remove age and gender from here since they'll be in text