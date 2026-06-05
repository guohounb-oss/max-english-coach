import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import get_settings

settings = get_settings()

_chroma_client = None
_conversation_collection = None
_vocabulary_collection = None
_grammar_collection = None


def get_chroma_client() -> chromadb.PersistentClient:
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _chroma_client


def get_conversation_collection():
    global _conversation_collection
    if _conversation_collection is None:
        client = get_chroma_client()
        _conversation_collection = client.get_or_create_collection(
            name="conversation_memories",
            metadata={"hnsw:space": "cosine"},
        )
    return _conversation_collection


def get_vocabulary_collection():
    global _vocabulary_collection
    if _vocabulary_collection is None:
        client = get_chroma_client()
        _vocabulary_collection = client.get_or_create_collection(
            name="vocabulary_memories",
            metadata={"hnsw:space": "cosine"},
        )
    return _vocabulary_collection


def get_grammar_collection():
    global _grammar_collection
    if _grammar_collection is None:
        client = get_chroma_client()
        _grammar_collection = client.get_or_create_collection(
            name="grammar_history",
            metadata={"hnsw:space": "cosine"},
        )
    return _grammar_collection
