import urllib.parse
import re
import hashlib
from django.conf import settings
from google import genai

def generate_detailed_art_prompt(note_title, note_text):
    """Uses Gemini 2.0 Flash to extract 2-3 precise visual keywords."""
    GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)
    
    if not GEMINI_KEY:
        return note_title

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "Extract 2 to 3 visual search keywords representing this study topic.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Rules: Output ONLY 2-3 plain keywords separated by spaces (e.g., 'computer code programming'). "
            "No quotes, no markdown, no extra text."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        raw_prompt = response.text.strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_prompt)
        return " ".join(cleaned_prompt.split()) or note_title

    except Exception as e:
        print(f"\n[Gemini API Warning] {e}")
        return note_title


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a context-accurate, distinct AI image URL using Pollinations.
    Uses an MD5 hash seed so the exact same image is locked permanently once saved in DB.
    """
    # 1. Get visual keywords from Gemini
    keywords = generate_detailed_art_prompt(note_title, note_text)
    
    # 2. Build a clear, simple prompt (e.g. "operating systems computer code wallpaper")
    clean_prompt = f"{keywords} study concept wallpaper"
    encoded_prompt = urllib.parse.quote(clean_prompt)
    
    # 3. Create a unique deterministic seed per note
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    seed = int(raw_hash, 16) % 999999
    
    # Pollinations turbo model renders in ~1s and respects the seed parameter
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={seed}&model=turbo"