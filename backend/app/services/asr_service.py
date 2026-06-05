"""本地语音识别 — faster-whisper (开源，离线运行)

首次运行会自动下载 tiny 模型（~75MB），后续秒级识别。
"""
import tempfile
import os
from app.core.config import get_settings

settings = get_settings()

# 延迟加载模型（首次调用时下载）
_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        # tiny 模型：最小最快，英文识别效果不错
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model


class AliyunASRService:
    """语音识别 — faster-whisper 本地引擎（保持同名类，兼容路由）"""

    async def transcribe(
        self, audio_bytes: bytes, filename: str = "audio.webm"
    ) -> str:
        """将音频转为英文文本"""
        # 写入临时文件
        suffix = f".{filename.rsplit('.', 1)[-1]}" if "." in filename else ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name

        try:
            model = _get_model()
            segments, _ = model.transcribe(tmp_path, language="en", beam_size=1)
            text = " ".join(seg.text.strip() for seg in segments)
            return text
        finally:
            os.unlink(tmp_path)
