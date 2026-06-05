from pathlib import Path


class PromptService:
    """Composes prompts dynamically from template files."""

    def __init__(self, prompts_dir: str = "./app/prompts"):
        self.prompts_dir = Path(prompts_dir)

    def _load(self, filename: str) -> str:
        path = self.prompts_dir / filename
        if path.exists():
            return path.read_text().strip()
        return ""

    def build_system_prompt(
        self,
        student_name: str = "Student",
        english_level: str = "intermediate",
        common_mistakes: str = "None yet",
        past_topics: str = "None yet",
        vocabulary_learned: str = "None yet",
        correction_frequency: str = "moderate",
        learning_mode: str = "free_conversation",
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

        if learning_mode == "business_english":
            parts.append(
                "Focus on professional vocabulary, email phrases, meeting language, "
                "and business small talk. Keep it practical."
            )
        elif learning_mode == "travel_english":
            parts.append(
                "Focus on travel scenarios: airports, hotels, restaurants, directions, "
                "shopping, and casual tourist conversations."
            )
        elif learning_mode == "interview_practice":
            parts.append(
                "Act as a job interviewer. Ask common interview questions. Give feedback "
                "on answers — clarity, confidence, and professional word choice."
            )
        elif learning_mode == "american_slang":
            parts.append(
                "Teach American slang and idioms naturally during conversation. "
                "Explain what they mean and when to use them."
            )
        elif learning_mode == "pronunciation_practice":
            parts.append(
                "Focus on pronunciation. Point out sounds that need work, demonstrate "
                "correct mouth positions, and celebrate improvements."
            )

        return "\n".join(parts)
