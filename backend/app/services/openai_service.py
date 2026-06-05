from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()


class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat(
        self,
        messages: list[dict],
        system_prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.8,
        max_tokens: int = 300,
    ) -> str:
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = await self.client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def analyze_corrections(
        self, user_text: str, assistant_response: str
    ) -> dict:
        """Analyze what corrections were made in the response."""
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

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
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

    async def generate_summary(self, messages: list[dict]) -> str:
        """Generate a conversation summary."""
        convo = "\n".join(
            [f"{m['role']}: {m['content']}" for m in messages[-20:]]
        )

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
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
