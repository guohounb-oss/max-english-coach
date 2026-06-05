from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()


class WhisperService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        """Transcribe audio bytes to English text."""
        response = await self.client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, audio_bytes, "audio/webm"),
            language="en",
            response_format="text",
        )
        return response.strip()
