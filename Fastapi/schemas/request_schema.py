from pydantic import BaseModel

class SymptomRequest(BaseModel):
    text: str
    language: str = "en"