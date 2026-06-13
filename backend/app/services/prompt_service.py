from pathlib import Path


class PromptService:
    """动态组合系统提示词 — 含生词本高频词注入 + 多种教学模式"""

    def __init__(self, prompts_dir: str = "./app/prompts"):
        self.prompts_dir = Path(prompts_dir)

    def _load(self, filename: str) -> str:
        path = self.prompts_dir / filename
        return path.read_text().strip() if path.exists() else ""

    def build_system_prompt(
        self,
        student_name: str = "Student",
        english_level: str = "intermediate",
        common_mistakes: str = "None yet",
        past_topics: str = "None yet",
        vocabulary_learned: str = "None yet",
        correction_frequency: str = "moderate",
        learning_mode: str = "free_conversation",
        wordbook_words: str = "",
    ) -> str:
        parts = [
            self._load("system_prompt.txt"),
            "",
            self._load("personality_rules.txt"),
            "",
            self._load("teacher_rules.txt").format(
                correction_frequency=correction_frequency
            ),
            "",
            self._load("memory_rules.txt").format(
                student_name=student_name,
                english_level=english_level,
                common_mistakes=common_mistakes,
                past_topics=past_topics,
                vocabulary_learned=vocabulary_learned,
            ),
            "",
            self._load("safety_rules.txt"),
            "",
            f"Current learning mode: {learning_mode}",
        ]

        # ── 生词本高频词注入 ──────────────────────────
        if wordbook_words:
            parts.append(
                "IMPORTANT: The student has saved these words in their wordbook. "
                "Try to naturally use these words in your responses to increase "
                f"the student's exposure: {wordbook_words}\n"
                "High-star (⭐) words should appear more frequently."
            )

        # ── 教学模式 ────────────────────────────────────
        mode_directives = {
            "daily_course": self._mode_daily_course,
            "flashcards": self._mode_flashcards,
            "grammar_decoder": self._mode_grammar_decoder,
            "quiz_assessment": self._mode_quiz,
            "business_english": self._mode_business,
            "travel_english": self._mode_travel,
            "interview_practice": self._mode_interview,
            "american_slang": self._mode_slang,
            "pronunciation_practice": self._mode_pronunciation,
        }

        directive = mode_directives.get(learning_mode)
        if directive:
            parts.append(directive())

        return "\n".join(parts)

    # ── 教学模式定义 ──────────────────────────────────

    def _mode_daily_course(self) -> str:
        return (
            "DAILY COURSE MODE — You are leading a structured 30-minute English lesson.\n"
            "1. Start with a warm-up question about the day's topic.\n"
            "2. Introduce 3-5 key vocabulary words with natural examples.\n"
            "3. Practice through conversation — correct mistakes gently.\n"
            "4. End with 2-3 review questions to check understanding.\n"
            "Keep the pace engaging and conversational, not lecture-like."
        )

    def _mode_flashcards(self) -> str:
        return (
            "FLASHCARD MODE — Convert vocabulary into memorable flashcards.\n"
            "For each word the student encounters:\n"
            "1. Show the word clearly.\n"
            "2. Give a simple, memorable Chinese translation.\n"
            "3. Provide a vivid example sentence.\n"
            "4. Share a quick memory trick (association, root, or funny image).\n"
            "Review previous words regularly using spaced repetition."
        )

    def _mode_grammar_decoder(self) -> str:
        return (
            "GRAMMAR DECODER MODE — Explain grammar rules simply.\n"
            "When a grammar question comes up:\n"
            "1. Explain the rule in plain, non-technical English.\n"
            "2. Give 3 clear examples.\n"
            "3. Highlight the 3 most common mistakes students make with this rule.\n"
            "4. Ask the student to try their own sentence using the rule.\n"
            "Make grammar feel like a life hack, not a textbook."
        )

    def _mode_quiz(self) -> str:
        return (
            "QUIZ MODE — Assess the student's progress.\n"
            "Based on the conversation so far:\n"
            "1. Create a 5-10 question quiz covering vocabulary and grammar discussed.\n"
            "2. Ask one question at a time, wait for the answer.\n"
            "3. After each answer, tell them if it's correct and explain briefly.\n"
            "4. At the end, give a total score and 1-2 areas to focus on.\n"
            "Keep it encouraging — this is about progress, not perfection."
        )

    def _mode_business(self) -> str:
        return (
            "Focus on professional vocabulary, email phrases, meeting language, "
            "and business small talk. Keep it practical."
        )

    def _mode_travel(self) -> str:
        return (
            "Focus on travel scenarios: airports, hotels, restaurants, directions, "
            "shopping, and casual tourist conversations."
        )

    def _mode_interview(self) -> str:
        return (
            "Act as a job interviewer. Ask common interview questions. Give feedback "
            "on answers — clarity, confidence, and professional word choice."
        )

    def _mode_slang(self) -> str:
        return (
            "Teach American slang and idioms naturally during conversation. "
            "Explain what they mean and when to use them."
        )

    def _mode_pronunciation(self) -> str:
        return (
            "Focus on pronunciation. Point out sounds that need work, demonstrate "
            "correct mouth positions, and celebrate improvements."
        )
