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
            "- Mathematics -> 'A futuristic holographic equation grid with geometric shapes and glowing formulas floating in space'\n"
            "- Chemistry -> 'A collection of illuminated laboratory flasks with colorful chemical reactions and molecular structures'\n"
            "- Biology -> 'A detailed 3D DNA double helix surrounded by glowing cells and microscopic biological elements'\n"
            "- History -> 'Ancient scrolls, maps, and artifacts arranged on a richly textured wooden desk with warm lighting'\n"
            "- Geography -> 'A futuristic globe with illuminated continents, topographic patterns, and digital location markers'\n"
            "- Economics -> 'A sleek financial dashboard with rising graphs, currency symbols, and market analytics displays'\n"
            "- Business Studies -> 'A modern corporate workspace featuring holographic charts, strategy boards, and growth metrics'\n"
            "- Accounting -> 'A professional ledger interface with glowing financial records, calculators, and balance sheets'\n"
            "- Computer Science -> 'A futuristic coding environment with floating code streams, servers, and digital data networks'\n"
            "- Artificial Intelligence -> 'An abstract neural network visualization with interconnected glowing nodes and flowing data paths'\n"
            "- Cybersecurity -> 'A digital shield protecting streams of encrypted data against a backdrop of futuristic technology'\n"
            "- Data Science -> 'A high-tech analytics dashboard displaying colorful data visualizations, charts, and predictive models'\n"
            "- Machine Learning -> 'An advanced neural network system processing dynamic datasets through glowing interconnected pathways'\n"
            "- Programming -> 'A sleek developer workstation with holographic code panels and illuminated software architecture diagrams'\n"
            "- Networking -> 'A global digital network map with connected servers, routers, and data transmission pathways'\n"
            "- Electronics -> 'A detailed circuit board with glowing components, microprocessors, and precision electronic pathways'\n"
            "- Mechanical Engineering -> 'A collection of precision gears, mechanical assemblies, and futuristic engineering blueprints'\n"
            "- Civil Engineering -> 'A modern city skyline emerging from detailed architectural plans and structural design models'\n"
            "- Electrical Engineering -> 'A dynamic power grid visualization with glowing electrical currents and advanced infrastructure'\n"
            "- Astronomy -> 'A breathtaking cosmic scene featuring planets, stars, telescopes, and deep-space phenomena'\n"
            "- Space Science -> 'A futuristic spacecraft orbiting a distant planet surrounded by nebulae and celestial objects'\n"
            "- Environmental Science -> 'A harmonious blend of lush ecosystems, renewable energy systems, and sustainable technology'\n"
            "- Medical Science -> 'A futuristic medical interface displaying anatomical models, diagnostics, and healthcare technology'\n"
            "- Psychology -> 'An abstract visualization of the human mind with interconnected thoughts, neural pathways, and cognitive patterns'\n"
            "- Literature -> 'An elegant collection of classic books with floating pages and glowing storytelling elements'\n"
            "- English -> 'An artistic arrangement of books, handwritten manuscripts, and illuminated typography'\n"
            "- Philosophy -> 'Ancient philosophical texts surrounded by abstract symbols and contemplative atmospheric lighting'\n"
            "- Law -> 'A professional legal desk featuring scales of justice, law books, and modern legal documents'\n"
            "- Political Science -> 'A global governance visualization with parliamentary architecture, policy documents, and world maps'\n"
            "- Sociology -> 'An interconnected network of diverse communities represented through abstract social relationship diagrams'\n"
            "- Statistics -> 'A modern analytics workspace with dynamic charts, probability distributions, and mathematical visualizations'\n"
            "- Finance -> 'A sophisticated financial trading interface with market trends, investment portfolios, and economic indicators'\n"
            "- Marketing -> 'A creative digital campaign dashboard with branding elements, audience analytics, and growth metrics'\n"
            "- Design -> 'A modern creative studio featuring color palettes, design tools, and artistic visual compositions'\n"
            "- Architecture -> 'A futuristic architectural model illuminated with detailed structural elements and urban design concepts'\n"
            "- Robotics -> 'An advanced robotic system with precision mechanics, sensors, and intelligent automation components'\n"
            "- Blockchain -> 'A decentralized digital ledger visualization with interconnected blocks and secure transaction pathways'\n"
            "- Cloud Computing -> 'A futuristic cloud infrastructure with floating servers, data streams, and scalable digital systems'\n"
            "- DevOps -> 'A seamless software deployment pipeline visualized through connected development and infrastructure systems'\n"
            "- Renewable Energy -> 'A clean energy landscape featuring solar panels, wind turbines, and sustainable power technology'\n"
            "- Agriculture -> 'A modern smart farming environment with precision agriculture systems and thriving crops'\n"
            "- Biotechnology -> 'Advanced genetic engineering equipment surrounded by DNA structures and scientific innovation'\n"
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
        return f"a vibrant 3D conceptual visual representation of {note_title}"

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