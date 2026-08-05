import urllib.parse
import re
import hashlib
from django.conf import settings
from google import genai

def generate_detailed_art_prompt(note_title, note_text):
    """Uses Gemini 2.0 to extract 2-3 visual keywords."""
    GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)
    
    if not GEMINI_KEY:
        return note_title

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "Extract 2 to 3 visual search keywords for an unsplash image query representing this topic.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Rules: Output ONLY 2-3 plain keywords separated by commas (e.g. 'computer,technology,code'). No quotes or extra text."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        raw_prompt = response.text.strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9,\s]', '', raw_prompt)
        return cleaned_prompt or note_title

    except Exception as e:
        print(f"\n[Gemini API Warning] {e}")
        return note_title


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a static keyword-based Unsplash URL with a signature seed.
    """
    keywords = generate_detailed_art_prompt(note_title, note_text)
    
    # 1. Format keywords into comma-separated query string
    sanitized = re.sub(r'\s+', '', keywords.strip().lower())
    encoded_keywords = urllib.parse.quote(sanitized)
    
    # 2. Hash seed locks the exact result from Unsplash
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    sig = int(raw_hash, 16) % 1000
    
    return f"https://source.unsplash.com/featured/800x400/?{encoded_keywords}&sig={sig}"