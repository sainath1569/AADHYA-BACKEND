import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

TRANSLATION_API = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-mul-en"


def translate_to_english(text: str):

    payload = {
        "inputs": text
    }

    response = requests.post(
        TRANSLATION_API,
        headers=HEADERS,
        json=payload
    )

    result = response.json()

    if isinstance(result, list):
        return result[0]["translation_text"]

    return text


def translate_from_english(text: str, target_lang: str):
    # For hackathon simplicity, return English.
    # Reverse translation can be added later.
    return text