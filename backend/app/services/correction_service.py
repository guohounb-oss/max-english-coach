from app.services.llm_service import LLMService


class CorrectionService:
    """英语纠错分析 — 调用 LLM 做结构化分析"""

    def __init__(self):
        self.llm = LLMService()

    async def analyze(self, user_text: str, assistant_response: str) -> dict:
        """分析用户消息，返回结构化纠错数据"""
        return self.llm.analyze_corrections(user_text, assistant_response)

    def should_correct(self, frequency: str, message_index: int) -> bool:
        """根据纠错频率设置判断是否应该纠错"""
        if frequency == "high":
            return True
        elif frequency == "low":
            return message_index % 5 == 0
        else:  # moderate
            return message_index % 3 == 0
