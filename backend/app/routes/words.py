"""单词本路由 — 翻译 + CRUD + 星级排序"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.db.sqlite import SessionLocal
from app.services.word_service import WordService
from app.models.models import WordBook
from sqlalchemy import select, func, desc

router = APIRouter(prefix="/api/words", tags=["words"])


class SaveWordRequest(BaseModel):
    word: str
    chinese: str = ""
    pronunciation: str = ""
    example: str = ""
    example_cn: str = ""


class StarRequest(BaseModel):
    stars: int  # 1-5


# ── 翻译 ──────────────────────────────────────────

@router.post("/translate")
async def translate_word(req: dict):
    """翻译单词：返回中文、音标、例句"""
    word = req.get("word", "").strip().lower()
    if not word:
        return {"word": word, "chinese": "", "pronunciation": "", "example": ""}

    svc = WordService()
    return await svc.translate(word)


# ── 生词本 CRUD ───────────────────────────────────

@router.get("/saved/{user_id}")
def get_wordbook(user_id: int, sort: str = "time"):
    """获取单词本。sort: 'time'（时间）或 'star'（星级）"""
    db = SessionLocal()
    try:
        if sort == "star":
            q = (
                select(WordBook)
                .where(WordBook.user_id == user_id)
                .order_by(desc(WordBook.stars), desc(WordBook.created_at))
            )
        else:
            q = (
                select(WordBook)
                .where(WordBook.user_id == user_id)
                .order_by(desc(WordBook.created_at))
            )

        words = db.execute(q).scalars().all()
        return {
            "words": [
                {
                    "id": w.id,
                    "word": w.word,
                    "chinese": w.chinese,
                    "pronunciation": w.pronunciation,
                    "example": w.example,
                    "stars": w.stars,
                    "created_at": w.created_at.isoformat() if w.created_at else "",
                }
                for w in words
            ]
        }
    finally:
        db.close()


@router.post("/saved/{user_id}")
def save_word(user_id: int, req: SaveWordRequest):
    """保存陌生单词到单词本。已存在则跳过"""
    db = SessionLocal()
    try:
        existing = db.execute(
            select(WordBook).where(
                WordBook.user_id == user_id, WordBook.word == req.word.lower()
            )
        ).scalar_one_or_none()

        if existing:
            return {"status": "already_saved", "id": existing.id}

        w = WordBook(
            user_id=user_id,
            word=req.word.lower(),
            chinese=req.chinese,
            pronunciation=req.pronunciation,
            example=req.example,
            stars=0,
        )
        db.add(w)
        db.commit()
        db.refresh(w)
        return {"status": "saved", "id": w.id}
    finally:
        db.close()


@router.patch("/saved/{word_id}/star")
def star_word(word_id: int, req: StarRequest):
    """给单词打星（1-5）"""
    db = SessionLocal()
    try:
        w = db.execute(select(WordBook).where(WordBook.id == word_id)).scalar_one_or_none()
        if not w:
            return {"status": "not_found"}
        w.stars = max(1, min(5, req.stars))
        db.commit()
        return {"status": "ok", "stars": w.stars}
    finally:
        db.close()


@router.delete("/saved/{word_id}")
def delete_word(word_id: int):
    """删除单词"""
    db = SessionLocal()
    try:
        w = db.execute(select(WordBook).where(WordBook.id == word_id)).scalar_one_or_none()
        if w:
            db.delete(w)
            db.commit()
            return {"status": "deleted"}
        return {"status": "not_found"}
    finally:
        db.close()
