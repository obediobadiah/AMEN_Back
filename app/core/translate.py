from deep_translator import GoogleTranslator
from typing import Dict, Optional, List

def translate_content(text: str, source: str = "auto", target: str = "en") -> str:
    if not text:
        return ""
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def multi_translate(text: str, source_lang: Optional[str] = None) -> Dict[str, str]:
    """
    Returns a dict with both 'en' and 'fr' versions by leveraging Google's auto-detection.
    It translates the input once to English and once to French.
    """
    if not text:
        return {"en": "", "fr": ""}
    
    # We ignore the source_lang hint and let Google's 'auto' feature handle it.
    # This is much more reliable than manual langdetect for short strings.
    en_ver = translate_content(text, source="auto", target="en")
    fr_ver = translate_content(text, source="auto", target="fr")
    
    # Heuristic: If one translation is identical to the input, 
    # and the other is different, we have a clear source.
    # But even if we don't, returning both from 'auto' is the safest bet.
    return {
        "en": en_ver,
        "fr": fr_ver
    }

def multi_translate_list(items: List[str]) -> Dict[str, List[str]]:
    """
    Translates a list of strings into a bilingual dict.
    """
    if not items:
        return {"en": [], "fr": []}
        
    en_items = [translate_content(item, source="auto", target="en") for item in items]
    fr_items = [translate_content(item, source="auto", target="fr") for item in items]
    
    return {
        "en": en_items,
        "fr": fr_items
    }
