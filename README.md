# NOTEon 📝

A clean, fast note-taking web app built with Django — write, search, and archive your notes from anywhere.

**Live app:** [note-on-two.vercel.app](https://note-on-two.vercel.app/)

---

## Features

- 🔐 **User accounts** — register and log in to keep your notes private
- 🗒️ **Dashboard** — see all your notes at a glance
- ➕ **Quick note creation** — add a new note in one click
- 🔍 **Search** — find notes instantly by keyword
- 📦 **Archive** — move notes out of your active dashboard without deleting them
- 🤖 **AI-assisted notes** — powered by Google Gemini (`google-genai`) and Hugging Face models for smart note features (e.g. summarization / assistance)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | [Django](https://www.djangoproject.com/) 5.x |
| Database | SQLite (default) — Postgres-ready via `psycopg2-binary` |
| AI | Google Gemini API (`google-genai`), Hugging Face (`huggingface_hub`) |
| Static files | WhiteNoise |
| Server | Gunicorn |
| Config | `python-dotenv` |
| Deployment | [Vercel](https://vercel.com/) |

## Project Structure

```
NOTEon/
├── noteon/            # Django project (settings, URLs, WSGI/ASGI config)
├── notes/             # Core Django app (models, views, templates for notes)
├── index.py           # Vercel serverless entrypoint
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── vercel.json         # Vercel deployment configuration
└── .gitignore / .vercelignore
```

## Getting Started Locally

### Prerequisites
- Python 3.10+
- A Google Gemini API key (and/or Hugging Face token) for AI features
- (Optional) PostgreSQL, if you'd rather not use the default SQLite database

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/nipuntamore/NOTEon.git
   cd NOTEon
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   # Uses SQLite by default — no DATABASE_URL needed.
   # To use Postgres instead, uncomment and set:
   # DATABASE_URL=postgres://user:password@localhost:5432/noteon
   GEMINI_API_KEY=your-gemini-api-key
   HUGGINGFACE_TOKEN=your-huggingface-token
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` in your browser.

## Deployment

The app is configured for deployment on **Vercel** via `vercel.json` and `index.py`, with **WhiteNoise** serving static files and **Gunicorn** as the production WSGI server. Set the environment variables above in your Vercel project settings before deploying.

## Contributing

Issues and pull requests are welcome. If you'd like to propose a significant change, please open an issue first to discuss what you'd like to change.

## License

No license has been specified for this repository yet. Until one is added, all rights are reserved by the author.

---

Built by [Nipun Tamore](https://github.com/nipuntamore)
