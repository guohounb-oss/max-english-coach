import datetime
from sqlalchemy import String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.sqlite import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), default="Student")
    english_level: Mapped[str] = mapped_column(String(50), default="intermediate")
    learning_mode: Mapped[str] = mapped_column(String(50), default="free_conversation")
    correction_frequency: Mapped[str] = mapped_column(String(20), default="moderate")
    voice_speed: Mapped[float] = mapped_column(Float, default=1.0)
    voice_volume: Mapped[float] = mapped_column(Float, default=1.0)
    total_minutes: Mapped[float] = mapped_column(Float, default=0.0)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    last_active: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")
    vocabulary: Mapped[list["Vocabulary"]] = relationship(back_populates="user")
    grammar_mistakes: Mapped[list["GrammarMistake"]] = relationship(back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    mode: Mapped[str] = mapped_column(String(50), default="free_conversation")
    summary: Mapped[str] = mapped_column(Text, default="")
    topic: Mapped[str] = mapped_column(String(200), default="")
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))  # user, assistant
    content: Mapped[str] = mapped_column(Text)
    corrections: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    vocabulary_suggestions: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    word: Mapped[str] = mapped_column(String(100))
    context: Mapped[str] = mapped_column(Text, default="")
    times_encountered: Mapped[int] = mapped_column(Integer, default=1)
    learned: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="vocabulary")


class GrammarMistake(Base):
    __tablename__ = "grammar_mistakes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    original: Mapped[str] = mapped_column(Text)
    correction: Mapped[str] = mapped_column(Text)
    rule: Mapped[str] = mapped_column(String(200), default="")
    times_made: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="grammar_mistakes")


class FluencyScore(Base):
    __tablename__ = "fluency_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    score: Mapped[float] = mapped_column(Float)  # 0-100
    vocabulary_count: Mapped[int] = mapped_column(Integer, default=0)
    grammar_errors: Mapped[int] = mapped_column(Integer, default=0)
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
