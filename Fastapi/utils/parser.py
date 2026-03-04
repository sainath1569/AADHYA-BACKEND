import re

def parse_symptoms_input(user_input: str):
    """
    Parse input text to extract symptoms, age, and gender
    Example: "Severe chest pain and difficulty breathing age 45 male"
    """
    # Initialize default values
    age = None
    gender = None
    symptoms_text = user_input
    
    # Convert to lowercase for easier parsing
    text_lower = user_input.lower()
    
    # Extract age using regex patterns
    age_patterns = [
        r'age\s+(\d{1,3})',           # "age 45"
        r'aged\s+(\d{1,3})',           # "aged 45"
        r'(\d{1,3})\s*years?',          # "45 years" or "45 year"
        r'(\d{1,3})\s*yr',              # "45 yr"
        r'\b(\d{1,3})\b(?=\s*(?:male|female|man|woman|old|years|yr))'  # number before gender
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, text_lower)
        if match:
            age = int(match.group(1))
            # Remove the age part from symptoms text
            age_text = match.group(0)
            symptoms_text = symptoms_text.replace(age_text, '').strip()
            break
    
    # If no age found with patterns, look for standalone numbers
    if age is None:
        # Look for numbers that might be age
        number_pattern = r'\b(\d{1,3})\b'
        matches = re.findall(number_pattern, text_lower)
        for num in matches:
            num_int = int(num)
            if 1 <= num_int <= 120:  # Valid age range
                age = num_int
                # Remove the number from symptoms text
                symptoms_text = re.sub(r'\b' + num + r'\b', '', symptoms_text).strip()
                break
    
    # Extract gender
    gender_keywords = {
        'male': ['male', 'man', 'boy', 'gentleman', 'mr', 'm'],
        'female': ['female', 'woman', 'girl', 'lady', 'ms', 'mrs', 'f']
    }
    
    words = symptoms_text.lower().split()
    for word in words:
        word_clean = word.strip('.,!?;:')
        if word_clean in gender_keywords['male']:
            gender = 'male'
            # Remove gender from symptoms text
            symptoms_text = re.sub(r'\b' + re.escape(word) + r'\b', '', symptoms_text, flags=re.IGNORECASE).strip()
            break
        elif word_clean in gender_keywords['female']:
            gender = 'female'
            symptoms_text = re.sub(r'\b' + re.escape(word) + r'\b', '', symptoms_text, flags=re.IGNORECASE).strip()
            break
    
    # Clean up symptoms text (remove extra spaces, punctuation at ends)
    symptoms_text = re.sub(r'\s+', ' ', symptoms_text).strip()
    symptoms_text = symptoms_text.strip('.,!?;:')
    
    # If symptoms_text becomes empty, use original
    if not symptoms_text:
        symptoms_text = user_input
    
    return {
        "symptoms": symptoms_text,
        "age": age,
        "gender": gender
    }