import urllib.parse
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
            "Examples:\n"
            "- Operating System -> 'A high-tech computer motherboard with glowing microchips and blue circuit lines'\n"
            "- Physics -> 'A glowing atomic structure surrounded by light orbits on a dark laboratory table'\n"
            "Rules: Output ONLY the visual description. No human faces, no text overlay."
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        # Gracefully handle 429 Rate Limit / Quota Exhaustion or transient errors
        print(f"\n[Gemini API Warning] {e}\nFalling back to default prompt generation...")
        return f"modern high tech computer hardware setup representing {note_title}"

def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a deterministic FLUX AI image URL via Pollinations.
    Uses the fallback visual prompt if Gemini hits its free tier rate limit.
    """
    visual_prompt = generate_detailed_art_prompt(note_title, note_text)
    
    # Stable seed so refreshing never reshuffles the cover
    deterministic_seed = abs(hash(f"{note_title}_{note_text}")) % 100000
    encoded_prompt = urllib.parse.quote(visual_prompt)
    
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true&seed={deterministic_seed}&model=flux"