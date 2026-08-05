import urllib.parse
import re
import hashlib
from django.conf import settings
from google import genai

def generate_detailed_art_prompt(note_title, note_text):
    """Uses Gemini 2.0 to extract 3-5 short visual keywords for fast image generation."""
    GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)
    
    if not GEMINI_KEY:
        return f"{note_title} technology concept"

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "You are an image prompt optimizer.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Output ONLY 3 to 5 core visual keywords describing this topic.\n"
            "Examples: 'computer motherboard server code', 'ancient historical architecture fort', 'dna strand laboratory'.\n"
            "Rules: Output strictly words separated by spaces. No punctuation, no sentences, no quotes."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        raw_prompt = response.text.strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_prompt)
        return " ".join(cleaned_prompt.split())

    except Exception as e:
        print(f"\n[Gemini API Warning] {e}\nFalling back to title keywords...")
        return f"{note_title} technology concept"


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a fast, deterministic AI image URL via Pollinations using short keywords.
    """
    visual_keywords = generate_detailed_art_prompt(note_title, note_text)
    
    # 1. Clean prompt text to plain letters, numbers, and spaces
    sanitized_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', visual_keywords).strip()
    
    # 2. Positive deterministic seed based on title & text
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    deterministic_seed = int(raw_hash, 16) % 99999
    
    # 3. Standard URL encoding for spaces (%20)
    encoded_prompt = urllib.parse.quote(sanitized_prompt)
    
    # Fast rendering endpoint using turbo model
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={deterministic_seed}&model=turbo"