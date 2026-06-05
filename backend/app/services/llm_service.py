from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """DeepSeek V3 LLM — OpenAI 兼容协议，只改 base_url 和 api_key"""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    def chat(
        self,
        messages: list[dict],
        system_prompt: str,
        model: str | None = None,
        temperature: float = 0.8,
        max_tokens: int = 300,
    ) -> str:
        model = model or settings.deepseek_model
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    def analyze_corrections(
        self, user_text: str, assistant_response: str
    ) -> dict:
        """分析助手回复中的纠错内容，返回结构化 JSON"""
        prompt = f"""
        Compare the user's original text with the assistant's correction.
        
        User said: "{user_text}"
        Assistant responded with corrections.
        
        Return a JSON object with:
        - corrections: list of {{original: str, corrected: str, rule: str}}
        - vocabulary_suggestions: list of {{weak_word: str, alternatives: [str]}}
        - grammar_issues: list of {{error: str, fix: str}}
        
        Only include actual corrections — if nothing was wrong, return empty arrays.
        Respond with ONLY valid JSON, no markdown.
        """

        response = self.client.chat.completions.create(
            model=settings.deepseek_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a grammar analysis tool. Return only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=400,
        )
        import json

        try:
            return json.loads(response.choices[0].message.content or "{}")
        except json.JSONDecodeError:
            return {"corrections": [], "vocabulary_suggestions": [], "grammar_issues": []}

    def generate_summary(self, messages: list[dict]) -> str:
        """生成对话摘要"""
        convo = "\n".join(
            [f"{m['role']}: {m['content']}" for m in messages[-20:]]
        )

        response = self.client.chat.completions.create(
            model=settings.deepseek_model,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize this English tutoring conversation in 2-3 sentences. "
                    "Include: main topic, notable corrections, and student's mood.",
                },
                {"role": "user", "content": convo},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        return response.choices[0].message.content or ""
