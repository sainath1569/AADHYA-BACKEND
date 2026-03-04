from pydantic import BaseModel

class SymptomRequest(BaseModel):
    text: str  # Only text field, no language