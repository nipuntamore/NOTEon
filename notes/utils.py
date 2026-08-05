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


import hashlib

def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a fast, unique, and permanent image URL per note using Picsum seeds.
    Does not time out, never triggers fallback, and remains identical across refreshes.
    """
    # Create a unique positive integer seed from the title and text
    unique_string = f"{note_title.strip().lower()}_{note_text.strip().lower()}"
    raw_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    seed = int(raw_hash, 16) % 100000
    
    return f"https://picsum.photos/seed/{seed}/800/400"