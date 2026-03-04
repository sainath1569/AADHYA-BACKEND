from transformers import pipeline

print("Loading DistilBERT model...")

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased"
)

print("Model loaded successfully!")


def classify_disease(text: str):
    try:
        result = classifier(text)

        label = result[0]["label"]
        confidence = result[0]["score"] * 100

        return {
            "predicted_condition": label,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        print("CLASSIFIER ERROR:", e)
        return {
            "predicted_condition": "Unknown",
            "confidence": 0
        }