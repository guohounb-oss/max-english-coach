import datetime
import json
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from app.models.models import (
    User,
    Conversation,
    Message,
    Vocabulary,
    GrammarMistake,
    FluencyScore,
    WordBook,
)
from app.db.chroma import (
    get_conversation_collection,
    get_vocabulary_collection,
    get_grammar_collection,
)


class MemoryService:
    """Manages both SQLite (structured) and ChromaDB (vector) memories."""

    def get_or_create_user(self, db: Session, user_id: int = 1) -> User:
        result = db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(id=user_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def update_user(self, db: Session, user_id: int, **kwargs) -> User:
        user = self.get_or_create_user(db, user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.last_active = datetime.datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def get_user_stats(self, db: Session, user_id: int) -> dict:
        user = self.get_or_create_user(db, user_id)

        vocab_result = db.execute(
            select(func.count(Vocabulary.id)).where(Vocabulary.user_id == user_id)
        )
        vocab_count = vocab_result.scalar() or 0

        grammar_result = db.execute(
            select(func.count(GrammarMistake.id)).where(
                GrammarMistake.user_id == user_id
            )
        )
        grammar_count = grammar_result.scalar() or 0

        conv_result = db.execute(
            select(func.count(Conversation.id)).where(
                Conversation.user_id == user_id
            )
        )
        conv_count = conv_result.scalar() or 0

        scores_result = db.execute(
            select(FluencyScore)
            .where(FluencyScore.user_id == user_id)
            .order_by(FluencyScore.recorded_at.desc())
            .limit(30)
        )
        scores = scores_result.scalars().all()

        return {
            "name": user.name,
            "level": user.english_level,
            "total_minutes": round(user.total_minutes, 1),
            "streak_days": user.streak_days,
            "vocabulary_learned": vocab_count,
            "grammar_mistakes_corrected": grammar_count,
            "total_conversations": conv_count,
            "fluency_trend": [
                {"date": s.recorded_at.isoformat(), "score": s.score} for s in scores
            ],
        }

    def save_conversation(
        self,
        db: Session,
        user_id: int,
        mode: str,
        messages: list[dict],
        duration_seconds: int = 0,
        summary: str = "",
        topic: str = "",
    ) -> Conversation:
        conv = Conversation(
            user_id=user_id,
            mode=mode,
            summary=summary,
            topic=topic,
            duration_seconds=duration_seconds,
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

        for msg in messages:
            m = Message(
                conversation_id=conv.id,
                role=msg["role"],
                content=msg["content"],
                corrections=msg.get("corrections"),
                vocabulary_suggestions=msg.get("vocabulary_suggestions"),
            )
            db.add(m)
        db.commit()

        # ChromaDB
        try:
            collection = get_conversation_collection()
            full_text = " ".join([m["content"] for m in messages if m["role"] == "user"])
            if full_text.strip():
                collection.add(
                    documents=[full_text],
                    metadatas=[{"user_id": str(user_id), "timestamp": datetime.datetime.utcnow().isoformat()}],
                    ids=[f"conv_{conv.id}"],
                )
        except Exception:
            pass

        return conv

    def get_recent_messages(self, db: Session, user_id: int, limit: int = 20) -> list[dict]:
        result = db.execute(
            select(Message)
            .join(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return [
            {"role": m.role, "content": m.content}
            for m in reversed(messages)
        ]

    def get_past_topics(self, db: Session, user_id: int) -> str:
        result = db.execute(
            select(Conversation.topic)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(10)
        )
        topics = [r for r in result.scalars().all() if r]
        return ", ".join(topics) if topics else "None yet"

    def track_vocabulary(self, db: Session, user_id: int, word: str, context: str = ""):
        result = db.execute(
            select(Vocabulary).where(
                and_(Vocabulary.user_id == user_id, Vocabulary.word == word)
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.times_encountered += 1
        else:
            entry = Vocabulary(user_id=user_id, word=word, context=context)
            db.add(entry)
        db.commit()

        try:
            collection = get_vocabulary_collection()
            collection.add(
                documents=[word],
                metadatas=[{"user_id": str(user_id), "context": context}],
                ids=[f"vocab_{user_id}_{word}"],
            )
        except Exception:
            pass

    def get_vocabulary_list(self, db: Session, user_id: int) -> list[dict]:
        result = db.execute(
            select(Vocabulary)
            .where(Vocabulary.user_id == user_id)
            .order_by(Vocabulary.times_encountered.desc())
            .limit(100)
        )
        vocab = result.scalars().all()
        return [
            {"word": v.word, "context": v.context, "times": v.times_encountered}
            for v in vocab
        ]

    def track_mistake(
        self, db: Session, user_id: int, original: str, correction: str, rule: str = ""
    ):
        result = db.execute(
            select(GrammarMistake).where(
                and_(
                    GrammarMistake.user_id == user_id,
                    GrammarMistake.original == original,
                )
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.times_made += 1
        else:
            entry = GrammarMistake(
                user_id=user_id, original=original, correction=correction, rule=rule
            )
            db.add(entry)
        db.commit()

        try:
            collection = get_grammar_collection()
            collection.add(
                documents=[f"{original} -> {correction} ({rule})"],
                metadatas=[{"user_id": str(user_id)}],
                ids=[f"grammar_{user_id}_{original[:30]}"],
            )
        except Exception:
            pass

    def get_common_mistakes(self, db: Session, user_id: int) -> str:
        result = db.execute(
            select(GrammarMistake)
            .where(GrammarMistake.user_id == user_id)
            .order_by(GrammarMistake.times_made.desc())
            .limit(5)
        )
        mistakes = result.scalars().all()
        if not mistakes:
            return "None yet"
        return "; ".join(
            [f"{m.original} → {m.correction}" for m in mistakes]
        )

    def get_vocabulary_learned_str(self, db: Session, user_id: int) -> str:
        result = db.execute(
            select(Vocabulary.word)
            .where(Vocabulary.user_id == user_id)
            .order_by(Vocabulary.times_encountered.desc())
            .limit(10)
        )
        words = result.scalars().all()
        return ", ".join(words) if words else "None yet"

    def record_fluency(
        self,
        db: Session,
        user_id: int,
        score: float,
        vocabulary_count: int,
        grammar_errors: int,
    ):
        entry = FluencyScore(
            user_id=user_id,
            score=score,
            vocabulary_count=vocabulary_count,
            grammar_errors=grammar_errors,
        )
        db.add(entry)
        db.commit()

    def search_similar_memories(self, query: str, user_id: int, n: int = 3) -> list[str]:
        try:
            collection = get_conversation_collection()
            results = collection.query(
                query_texts=[query],
                n_results=n,
                where={"user_id": str(user_id)},
            )
            if results and results["documents"] and results["documents"][0]:
                return results["documents"][0]
        except Exception:
            pass
        return []

    def get_wordbook_words_str(self, db: Session, user_id: int) -> str:
        """获取生词本中高星级词汇，注入到提示词中提高出现频率"""
        result = db.execute(
            select(WordBook)
            .where(WordBook.user_id == user_id)
            .order_by(WordBook.stars.desc(), WordBook.created_at.desc())
            .limit(20)
        )
        words = result.scalars().all()
        if not words:
            return ""

        high_star = [f"⭐{w.stars} {w.word}" for w in words if w.stars >= 3]
        low_star = [w.word for w in words if w.stars < 3]
        all_words = high_star + low_star
        return ", ".join(all_words[:15])
