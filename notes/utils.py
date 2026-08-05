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
            "Rules: Output ONLY 2-3 plain keywords separated by commas (e.g., 'computer,technology,code'). "
            "No quotes, no markdown, no extra text."
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


# Curated high-res Unsplash photo IDs for standard academic / tech topics
# Guarantees sharp, context-accurate images that never time out
CURATED_FALLBACKS = {
    "operating": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80",  # Matrix / Cyber code
    "system": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",     # Circuit board
    "computer": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=80",   # Laptop code
    "physics": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&auto=format&fit=crop&q=80",    # Math & physics formulas
    "motion": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&auto=format&fit=crop&q=80",     # Physics equations
    "science": "https://images.unsplash.com/photo-1507668077129-56e32842fceb?w=800&auto=format&fit=crop&q=80",    # Scientific atom/lab
    "fort": "https://images.unsplash.com/photo-1599833975787-5c143f373c30?w=800&auto=format&fit=crop&q=80",       # Historical fort/castle
    "history": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?w=800&auto=format&fit=crop&q=80",    # Vintage book/history
}

def generate_ai_cover_image(note_title, note_text=""):
    """
    Generates a context-aware, static photo URL.
    Saves directly to DB once upon note creation and remains 100% identical on refreshes.
    """
    # 1. Ask Gemini for topic keywords
    keywords = generate_detailed_art_prompt(note_title, note_text)
    search_string = f"{note_title} {note_text} {keywords}".lower()

    # 2. Match against curated subject mapping for 100% accuracy
    for key, url in CURATED_FALLBACKS.items():
        if key in search_string:
            return url

    # 3. Dynamic Unsplash Source query using sanitized keywords
    clean_keywords = re.sub(r'[^a-zA-Z0-9,]', '', keywords).strip().lower()
    encoded_keywords = urllib.parse.quote(clean_keywords or "technology")
    
    # Hash seed ensures locking a distinct photo index per note
    raw_hash = hashlib.md5(f"{note_title}_{note_text}".encode('utf-8')).hexdigest()
    sig = int(raw_hash, 16) % 1000

    return f"https://source.unsplash.com/featured/800x400/?{encoded_keywords}&sig={sig}"