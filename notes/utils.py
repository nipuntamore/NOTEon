import urllib.parse
import re
import hashlib
from django.conf import settings
from google import genai

def generate_detailed_art_prompt(note_title, note_text):
    """Uses Gemini 2.0 to draft an image prompt with automatic fallback on 429 quota exhaustion."""
    GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)
    
    # Fallback default if API key is missing
    if not GEMINI_KEY:
        return f"modern clean illustration of {note_title}"

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "You are an art director generating image prompts for study notes.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Create a vivid, 1-sentence prompt describing a sleek photographic visual representing this topic.\n"
            "Rules: Output ONLY raw text. No quotes, no markdown, no punctuation, no dashes."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        raw_prompt = response.text.strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_prompt)
        return " ".join(cleaned_prompt.split())

    except Exception as e:
        print(f"\n[Gemini API Warning] {e}\nFalling back to default prompt generation...")
        return f"modern clean concept of {note_title}"


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a deterministic AI image URL via Pollinations (Turbo Engine).
    Fallback uses Unsplash tech/minimal visual instead of random cars/buildings.
    """
    visual_prompt = generate_detailed_art_prompt(note_title, note_text)
    
    # 1. Clean prompt text to simple words
    sanitized_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', visual_prompt).strip()
    
    # 2. Positive deterministic seed
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    deterministic_seed = int(raw_hash, 16) % 99999
    
    # 3. Standard %20 space encoding for Pollinations URL paths
    encoded_prompt = urllib.parse.quote(sanitized_prompt)
    
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={deterministic_seed}"