from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    detected = translator.detect(text)
    if detected.lang != "en":
        translated = translator.translate(text, dest="en")
        return translated.text
    return text


def translate_from_english(text, dest_lang):
    translated = translator.translate(text, dest=dest_lang)
    return translated.text