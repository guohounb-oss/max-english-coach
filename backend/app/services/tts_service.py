"""本地语音合成 — edge-tts (微软免费，无需 API Key)

使用微软 Edge 浏览器同款 TTS 引擎。支持多种自然英文女声。
"""
import base64
import tempfile
import os
import asyncio
from app.core.config import get_settings

settings = get_settings()


class VolcanoTTSService:
    """语音合成 — edge-tts 引擎（保持同名类，兼容路由）

    推荐英文女声:
      - en-US-AvaMultilingualNeural   Ava (美式，自然)
      - en-US-JennyNeural             Jenny (美式女声，经典)
      - en-US-AriaNeural              Aria (美式女声，清晰)
      - en-GB-SoniaNeural             Sonia (英式女声)
    """

    VOICE = "en-US-JennyNeural"

    async def generate_speech(
        self,
        text: str,
        voice: str | None = None,
        speed: float | None = None,
    ) -> bytes:
        """生成语音，返回 raw mp3 bytes"""
        import edge_tts

        selected_voice = voice or self.VOICE
        selected_speed = speed if speed is not None else settings.voice_speed

        # edge-tts 语速格式: "+10%" 或 "-20%"
        rate_str = f"{int((selected_speed - 1) * 100):+d}%"

        communicate = edge_tts.Communicate(text, selected_voice, rate=rate_str)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name

        try:
            await communicate.save(tmp_path)
            with open(tmp_path, "rb") as f:
                return f.read()
        finally:
            os.unlink(tmp_path)

    async def generate_speech_b64(
        self, text: str, voice: str | None = None
    ) -> str:
        """生成语音，返回 base64 字符串"""
        audio_bytes = await self.generate_speech(text, voice=voice)
        return base64.b64encode(audio_bytes).decode("utf-8")
