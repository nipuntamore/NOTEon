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
        return f"sleek modern technological setup representing {note_title}"

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "You are an art director generating image prompts for study notes.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Create a vivid, 1-sentence prompt describing a sleek photographic visual representing this topic.\n"
            "Rules: Output ONLY the raw visual description text. No quotes, no markdown, no dashes, no meta text."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        raw_prompt = response.text.strip()
        # Clean quotes and unwanted symbols out of Gemini output
        cleaned_prompt = re.sub(r'[\r\n"\'`\-\->]', ' ', raw_prompt)
        return " ".join(cleaned_prompt.split())

    except Exception as e:
        print(f"\n[Gemini API Warning] {e}\nFalling back to default prompt generation...")
        return f"a vibrant 3D conceptual visual representation of {note_title}"


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a deterministic FLUX AI image URL via Pollinations.
    Ensures safe URL encoding and positive seed generation.
    """
    visual_prompt = generate_detailed_art_prompt(note_title, note_text)
    
    # 1. Sanitize prompt text to plain letters, numbers, spaces, and commas
    sanitized_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_prompt)
    
    # 2. Stable, non-negative integer seed using MD5 hash (prevents Python runtime seed drift)
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    deterministic_seed = int(raw_hash, 16) % 100000
    
    # 3. Strictly encode all non-alphanumeric characters for the URL path
    encoded_prompt = urllib.parse.quote(sanitized_prompt, safe='')
    
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={deterministic_seed}&model=flux"