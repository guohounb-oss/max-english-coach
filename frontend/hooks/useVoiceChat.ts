"use client";

import { useCallback } from "react";
import { useStore } from "../lib/store";
import { useAudioRecorder } from "./useAudioRecorder";
import { sendVoiceChat } from "../lib/api";
import { playAudioFromBase64 } from "../lib/audio";

export function useVoiceChat() {
  const {
    addMessage,
    setRecording,
    setProcessing,
    setSpeaking,
    settings,
    messages,
  } = useStore();

  const { isRecording, startRecording, stopRecording, error } = useAudioRecorder();

  const pushToTalk = useCallback(async () => {
    if (isRecording) {
      // Stop recording and process
      setRecording(false);
      setProcessing(true);

      try {
        const audioBlob = await stopRecording();
        if (!audioBlob || audioBlob.size < 100) {
          setProcessing(false);
          return;
        }

        // Add user message placeholder (we'll get transcription from server)
        addMessage({
          id: "",
          role: "user",
          text: "...",
          timestamp: Date.now(),
        });

        const result = await sendVoiceChat(audioBlob, settings.learning_mode);

        // Update user message with actual transcription
        // (The backend returns AI text, we'd need a separate field for user transcript)
        // For simplicity, we show what we got

        const aiMsg = {
          id: "",
          role: "assistant" as const,
          text: result.text,
          corrections: result.corrections,
          vocabularySuggestions: result.vocabulary_suggestions,
          timestamp: Date.now(),
        };

        addMessage(aiMsg);

        // Play audio
        if (result.audio_b64) {
          setSpeaking(true);
          await playAudioFromBase64(result.audio_b64, settings.voice_volume);
          setSpeaking(false);
        }
      } catch (err) {
        console.error("Voice chat error:", err);
        addMessage({
          id: "",
          role: "assistant",
          text: "Sorry, something went wrong. Try again?",
          timestamp: Date.now(),
        });
      } finally {
        setProcessing(false);
      }
    } else {
      // Start recording
      setRecording(true);
      await startRecording();
    }
  }, [
    isRecording,
    startRecording,
    stopRecording,
    setRecording,
    setProcessing,
    setSpeaking,
    settings,
    addMessage,
  ]);

  return {
    isRecording,
    isProcessing: useStore((s) => s.isProcessing),
    isSpeaking: useStore((s) => s.isSpeaking),
    pushToTalk,
    error,
  };
}
