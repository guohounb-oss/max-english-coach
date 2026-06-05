from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.sqlite import SessionLocal
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/api/memory", tags=["memory"])


class UpdateUserRequest(BaseModel):
    name: str | None = None
    english_level: str | None = None
    learning_mode: str | None = None
    correction_frequency: str | None = None
    voice_speed: float | None = None
    voice_volume: float | None = None


@router.get("/user/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    try:
        memory = MemoryService()
        user = memory.get_or_create_user(db, user_id)
        return {
            "id": user.id,
            "name": user.name,
            "english_level": user.english_level,
            "learning_mode": user.learning_mode,
            "correction_frequency": user.correction_frequency,
            "voice_speed": user.voice_speed,
            "voice_volume": user.voice_volume,
        }
    finally:
        db.close()


@router.patch("/user/{user_id}")
def update_user(user_id: int, req: UpdateUserRequest):
    db = SessionLocal()
    try:
        memory = MemoryService()
        updates = {k: v for k, v in req.model_dump().items() if v is not None}
        memory.update_user(db, user_id, **updates)
        return {"status": "ok"}
    finally:
        db.close()


@router.get("/vocabulary/{user_id}")
def get_vocabulary(user_id: int):
    db = SessionLocal()
    try:
        memory = MemoryService()
        return memory.get_vocabulary_list(db, user_id)
    finally:
        db.close()


@router.get("/mistakes/{user_id}")
def get_mistakes(user_id: int):
    db = SessionLocal()
    try:
        memory = MemoryService()
        mistakes = memory.get_common_mistakes(db, user_id)
        return {"mistakes": mistakes}
    finally:
        db.close()


@router.get("/search")
def search_memories(query: str, user_id: int = 1, n: int = 3):
    memory = MemoryService()
    results = memory.search_similar_memories(query, user_id, n)
    return {"results": results}
