"""单词服务 — 翻译 + 生词本管理"""

from app.services.llm_service import LLMService
from app.core.config import get_settings

settings = get_settings()


class WordService:
    """单词翻译与生词本"""

    def __init__(self):
        self.llm = LLMService()

    async def translate(self, word: str) -> dict:
        """用 DeepSeek 翻译单词，返回中文意思 + 音标 + 例句"""
        prompt = f"""Translate this English word to Chinese. Return ONLY a JSON object:
{{
  "word": "{word}",
  "chinese": "中文意思",
  "pronunciation": "音标（IPA格式，如 /ˈeksəmpəl/）",
  "example": "一个地道英文例句",
  "example_cn": "例句中文翻译"
}}
Only return the JSON, no markdown, no extra text."""

        result_text = self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="You are a professional English-Chinese dictionary. Return only valid JSON.",
            temperature=0.1,
            max_tokens=200,
        )

        import json

        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {
                "word": word,
                "chinese": "",
                "pronunciation": "",
                "example": "",
                "example_cn": "",
            }

    async def translate_batch(self, words: list[str]) -> list[dict]:
        """批量翻译"""
        results = []
        for w in words[:10]:  # 最多一次 10 个
            r = await self.translate(w)
            results.append(r)
        return results
