import urllib.parse
import re
import hashlib
from django.conf import settings
from google import genai

def generate_detailed_art_prompt(note_title, note_text):
    """Uses Gemini 2.0 Flash to extract 2-3 precise, concrete visual keywords.

    Falls back to a generic 'notebook study desk' prompt (NOT the raw title)
    when Gemini is unavailable or returns something unusable, since abstract
    titles like "OS Notes" or "Assignment 2" give the image model nothing to
    draw and it improvises an unrelated image instead.
    """
    FALLBACK_PROMPT = "notebook desk study minimal"
    GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)

    if not GEMINI_KEY:
        print("[Gemini API Warning] GEMINI_API_KEY is not set — using generic fallback prompt")
        return FALLBACK_PROMPT

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        prompt = (
            "Extract 2 to 3 concrete, physically drawable visual keywords representing "
            "this study topic — real objects, symbols, or scenes an illustrator could draw. "
            "Avoid abstract or meta words like 'notes', 'assignment', 'project', 'study', 'concept'.\n"
            f"Title: {note_title}\n"
            f"Content: {note_text}\n\n"
            "Rules: Output ONLY 2-3 plain keywords separated by spaces (e.g., 'computer code programming'). "
            "No quotes, no markdown, no extra text, no full sentences."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        raw_prompt = (response.text or "").strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_prompt)
        words = cleaned_prompt.split()

        # Reject anything that isn't a short keyword list (e.g. Gemini echoing
        # back a sentence, an apology, or an empty response).
        if not (1 <= len(words) <= 6):
            print(f"[Gemini API Warning] Unusable keyword output: {raw_prompt!r} — using fallback prompt")
            return FALLBACK_PROMPT

        return " ".join(words)

    except Exception as e:
        print(f"[Gemini API Warning] {e}")
        return FALLBACK_PROMPT


def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a context-accurate, distinct AI image URL using Pollinations.
    Uses an MD5 hash seed so the exact same image is locked permanently once saved in DB.
    """
    # 1. Get visual keywords from Gemini
    keywords = generate_detailed_art_prompt(note_title, note_text)
    
    # 2. Build a clear, simple prompt (e.g. "operating systems computer code wallpaper")
    clean_prompt = f"{keywords}, flat illustration, minimal wallpaper"
    encoded_prompt = urllib.parse.quote(clean_prompt)
    
    # 3. Create a unique deterministic seed per note
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    seed = int(raw_hash, 16) % 999999
    
    # flux has noticeably better prompt adherence than turbo (turbo trades
    # accuracy for ~1s speed); worth the extra ~2s given how often turbo
    # drifted off-topic
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={seed}&model=flux"