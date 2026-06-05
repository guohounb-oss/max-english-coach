# Max English Coach — AI English Teacher

> "You're getting your point across. A more natural way would be..."

A voice-first AI English teacher with personality. Talk to Maxine — a witty, encouraging coach inspired by the energy of a sarcastic New York waitress. She corrects your English naturally, remembers your conversations, and makes learning feel like chatting with a funny friend.

---

## Features

- 🎤 **Voice-First**: Push-to-talk — speak naturally, get voice responses
- ✏️ **Natural Corrections**: Mistakes corrected in-flow, not like a textbook
- 📚 **Vocabulary Coaching**: Alternatives for weak/repeated words
- 🧠 **Conversation Memory**: Remembers your name, hobbies, past topics
- 📊 **Progress Dashboard**: Minutes, vocabulary, grammar fixes, fluency trends
- 🎭 **6 Learning Modes**: Free chat, Business, Travel, Interviews, Slang, Pronunciation
- 🌙 **Dark Mode**: Modern, clean UI built with Next.js + Tailwind

---

## Tech Stack

| Layer      | Technology                 |
| ---------- | -------------------------- |
| Frontend   | Next.js 15, TypeScript, TailwindCSS |
| Backend    | Python 3.12, FastAPI       |
| AI         | OpenAI GPT-4o, Whisper, TTS |
| Memory     | SQLite + ChromaDB           |
| Container  | Docker, docker-compose      |

---

## Quick Start

### Prerequisites

- Node.js 22+
- Python 3.12+
- An OpenAI API key (with access to GPT-4o, Whisper, TTS)

### 1. Clone & Setup

```bash
cd max-english-coach

# Copy environment file
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY
```

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

> **Note:** Uses pnpm (install with `npm install -g pnpm`). npm v11 has a resolution bug with tailwindcss.

### 4. Open

Navigate to **http://localhost:3000**

Press the mic button and start talking!

---

## Docker

```bash
# Set your API key
export OPENAI_API_KEY=sk-...

# Start everything
docker-compose up --build

# Open http://localhost:3000
```

---

## API Endpoints

| Endpoint             | Description                    |
| -------------------- | ------------------------------ |
| `POST /api/voice/chat`  | Voice chat — audio in, audio out |
| `POST /api/voice/transcribe` | Audio to text only |
| `POST /api/voice/tts`      | Text to speech |
| `GET /api/memory/user/:id` | Get user profile |
| `PATCH /api/memory/user/:id` | Update settings |
| `GET /api/dashboard/stats/:id` | Progress stats |

---

## Learning Modes

| Mode            | Focus                                          |
| --------------- | ---------------------------------------------- |
| Free Conversation | Casual chat, no topic constraints             |
| Business English  | Meeting language, emails, professional tone   |
| Travel English    | Airports, hotels, restaurants, directions     |
| Interview Practice | Mock interviews with feedback               |
| American Slang    | Idioms, slang, cultural expressions          |
| Pronunciation     | Sound work, mouth positions, accent coaching  |

---

## Project Structure

```
max-english-coach/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── core/config.py       # Settings (env vars)
│   │   ├── routes/              # API endpoints
│   │   │   ├── voice.py         # Voice chat + TTS
│   │   │   ├── memory.py        # User + vocabulary
│   │   │   └── dashboard.py     # Stats
│   │   ├── services/            # Business logic
│   │   │   ├── openai_service.py   # GPT-4o chat
│   │   │   ├── whisper_service.py  # Speech-to-text
│   │   │   ├── tts_service.py      # Text-to-speech
│   │   │   ├── prompt_service.py   # Prompt composition
│   │   │   ├── correction_service.py # Error analysis
│   │   │   └── memory_service.py    # SQLite + ChromaDB
│   │   ├── models/models.py     # SQLAlchemy models
│   │   ├── db/                  # Database layer
│   │   └── prompts/             # Prompt templates
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main app UI
│   │   ├── layout.tsx
│   │   └── components/          # React components
│   ├── hooks/                   # useVoiceChat, useAudioRecorder
│   ├── lib/                     # API client, store, utils
│   ├── Dockerfile
│   └── package.json
├── prompts/max_teacher.txt
├── docker-compose.yml
└── .env.example
```

---

## Configuration

All settings are in `.env`:

```
OPENAI_API_KEY=sk-...           # Required
CORRECTION_FREQUENCY=moderate    # low | moderate | high
DEFAULT_LEARNING_MODE=free_conversation
VOICE_SPEED=1.0
VOICE_VOLUME=1.0
```

---

## Logs

Logs are stored in `backend/logs/`:
- `system.log` — Server events
- `conversation.log` — Chat transcripts
- `error.log` — Errors

---

## License

MIT
