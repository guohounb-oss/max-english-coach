from fastapi import APIRouter
from app.db.sqlite import SessionLocal
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats/{user_id}")
def get_stats(user_id: int):
    db = SessionLocal()
    try:
        memory = MemoryService()
        return memory.get_user_stats(db, user_id)
    finally:
        db.close()
