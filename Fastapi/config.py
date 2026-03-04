import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "triage_db"
COLLECTION_NAME = "triage_logs"

CANDIDATE_LABELS = [
    "Cardiac condition",
    "Respiratory disease",
    "Infectious disease",
    "Neurological disorder",
    "General illness"
]