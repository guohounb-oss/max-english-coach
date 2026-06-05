from fastapi import APIRouter, UploadFile, File, Form
from app.db.sqlite import SessionLocal
from app.services.llm_service import LLMService
from app.services.asr_service import AliyunASRService
from app.services.tts_service import VolcanoTTSService
from app.services.prompt_service import PromptService
from app.services.correction_service import CorrectionService
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/api/voice", tags=["voice"])


@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    user_id: int = Form(default=1),
    mode: str = Form(default="free_conversation"),
):
    """主语音聊天端点：音频入 → DeepSeek → 火山引擎 TTS 音频出"""
    db = SessionLocal()
    try:
        memory = MemoryService()
        llm_svc = LLMService()
        asr_svc = AliyunASRService()
        tts_svc = VolcanoTTSService()
        prompt_svc = PromptService()
        correction_svc = CorrectionService()

        # 1. 阿里云 ASR 语音转文字
        audio_bytes = await audio.read()
        user_text = await asr_svc.transcribe(
            audio_bytes, filename=audio.filename or "audio.webm"
        )

        if not user_text.strip():
            return {"text": "", "audio_b64": "", "corrections": []}

        # 2. 获取用户上下文
        user = memory.get_or_create_user(db, user_id)
        past_topics = memory.get_past_topics(db, user_id)
        common_mistakes = memory.get_common_mistakes(db, user_id)
        vocab_learned = memory.get_vocabulary_learned_str(db, user_id)

        # 3. 构建系统提示词
        system_prompt = prompt_svc.build_system_prompt(
            student_name=user.name,
            english_level=user.english_level,
            common_mistakes=common_mistakes,
            past_topics=past_topics,
            vocabulary_learned=vocab_learned,
            correction_frequency=user.correction_frequency,
            learning_mode=mode,
        )

        # 4. 获取对话历史
        recent_msgs = memory.get_recent_messages(db, user_id)

        # 5. DeepSeek V3 生成回复
        messages = recent_msgs + [{"role": "user", "content": user_text}]
        ai_text = llm_svc.chat(messages=messages, system_prompt=system_prompt)

        # 6. 分析纠错
        corrections = await _analyze_corrections_llm(
            correction_svc, user_text, ai_text
        )

        # 7. 火山引擎 TTS 生成语音
        audio_b64 = await tts_svc.generate_speech_b64(ai_text)

        # 8. 保存到记忆
        memory.save_conversation(
            db=db,
            user_id=user_id,
            mode=mode,
            messages=[
                {"role": "user", "content": user_text},
                {
                    "role": "assistant",
                    "content": ai_text,
                    "corrections": corrections,
                },
            ],
            topic=user_text[:200],
        )

        # 9. 追踪词汇
        if corrections.get("vocabulary_suggestions"):
            for vs in corrections["vocabulary_suggestions"]:
                weak = vs.get("weak_word", "")
                if weak:
                    memory.track_vocabulary(db, user_id, weak)

        # 10. 追踪语法错误
        if corrections.get("corrections"):
            for c in corrections["corrections"]:
                memory.track_mistake(
                    db,
                    user_id,
                    c.get("original", ""),
                    c.get("corrected", ""),
                    c.get("rule", ""),
                )

        return {
            "text": ai_text,
            "audio_b64": audio_b64,
            "corrections": corrections.get("corrections", []),
            "vocabulary_suggestions": corrections.get(
                "vocabulary_suggestions", []
            ),
        }
    finally:
        db.close()


async def _analyze_corrections_llm(
    correction_svc: CorrectionService,
    user_text: str,
    ai_text: str,
) -> dict:
    """用 LLM 分析纠错（离线推理，不走 OpenAI）"""
    return await correction_svc.analyze(user_text, ai_text)


@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """仅语音转文字"""
    asr_svc = AliyunASRService()
    audio_bytes = await audio.read()
    text = await asr_svc.transcribe(
        audio_bytes, filename=audio.filename or "audio.webm"
    )
    return {"text": text}


@router.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    voice: str = Form(default="en_female_amanda"),
    speed: float = Form(default=1.0),
):
    """文字转语音"""
    tts_svc = VolcanoTTSService()
    audio_b64 = await tts_svc.generate_speech_b64(text, voice=voice)
    return {"audio_b64": audio_b64}
