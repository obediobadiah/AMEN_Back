from deep_translator import GoogleTranslator
from typing import Dict, Optional

def translate_content(text: str, source: str = "fr", target: str = "en") -> str:
    if not text:
        return ""
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text # Fallback to source text if translation fails

def multi_translate(text: str, source_lang: str) -> Dict[str, str]:
    """
    Given a text and its source language, return a dict with both 'en' and 'fr' versions.
    """
    if source_lang == "fr":
        return {
            "fr": text,
            "en": translate_content(text, source="fr", target="en")
        }
    else:
        return {
            "en": text,
            "fr": translate_content(text, source="en", target="fr")
        }
