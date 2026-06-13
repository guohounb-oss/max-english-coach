"use client";

import { useState, useCallback } from "react";
import { cn } from "../../lib/utils";
import { playAudioFromBase64 } from "../../lib/audio";
import { Volume2, RotateCcw } from "lucide-react";
import { WordPopup, type WordData } from "./WordPopup";

interface ChatBubbleProps {
  role: "user" | "assistant";
  text: string;
  audioB64?: string;
  isPlaying?: boolean;
}

export function ChatBubble({
  role,
  text,
  audioB64,
  isPlaying,
}: ChatBubbleProps) {
  const isUser = role === "user";
  const [replaying, setReplaying] = useState(false);
  const [popupWord, setPopupWord] = useState<string | null>(null);
  const [popupPos, setPopupPos] = useState({ x: 0, y: 0 });

  const handleReplay = async () => {
    if (!audioB64 || replaying) return;
    setReplaying(true);
    try {
      await playAudioFromBase64(audioB64);
    } catch (e) {
      console.error("Replay failed:", e);
    } finally {
      setReplaying(false);
    }
  };

  const handleWordClick = useCallback(
    (word: string, e: React.MouseEvent) => {
      // Only for assistant messages
      if (isUser) return;
      const clean = word.replace(/[^a-zA-Z'-]/g, "");
      if (clean.length < 2) return;
      setPopupWord(clean);
      setPopupPos({ x: e.clientX, y: e.clientY });
    },
    [isUser]
  );

  const handleSaveWord = async (data: WordData) => {
    try {
      await fetch("http://localhost:8000/api/words/saved/1", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    } catch (e) {
      console.error("Save word failed:", e);
    }
  };

  const renderText = (t: string) => {
    if (isUser) return <span>{t}</span>;

    // Split on word boundaries, keep punctuation
    const parts = t.split(/(\s+)/);
    return parts.map((part, i) => {
      if (/^\s+$/.test(part)) return part;
      const clean = part.replace(/[^a-zA-Z'-]/g, "");
      const punctuation = part.slice(clean.length);
      return (
        <span key={i}>
          <span
            onClick={(e) => handleWordClick(clean, e)}
            className="cursor-pointer hover:text-accent hover:underline decoration-accent/50 underline-offset-2 transition-colors"
            title="点击查看翻译"
          >
            {clean}
          </span>
          {punctuation}
        </span>
      );
    });
  };

  return (
    <>
      <div
        className={cn(
          "flex gap-3 animate-slide-up",
          isUser ? "justify-end" : "justify-start"
        )}
      >
        {!isUser && (
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-xs font-bold shrink-0">
            M
          </div>
        )}

        <div
          className={cn(
            "max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
            isUser
              ? "bg-primary text-primary-foreground rounded-br-md"
              : "bg-secondary text-secondary-foreground rounded-bl-md"
          )}
        >
          <div className="flex items-center gap-2">
            <span>{renderText(text)}</span>
            {isPlaying && (
              <Volume2 className="w-4 h-4 animate-pulse text-accent shrink-0" />
            )}
          </div>
        </div>

        {!isUser && audioB64 && (
          <button
            onClick={handleReplay}
            disabled={replaying}
            className="self-end mb-1 p-1.5 rounded-full hover:bg-secondary text-muted-foreground hover:text-accent transition-colors shrink-0"
            title="重播"
          >
            <RotateCcw
              className={cn("w-3.5 h-3.5", replaying && "animate-spin")}
            />
          </button>
        )}

        {isUser && (
          <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-bold shrink-0">
            U
          </div>
        )}
      </div>

      {popupWord && (
        <WordPopup
          word={popupWord}
          x={popupPos.x}
          y={popupPos.y}
          onClose={() => setPopupWord(null)}
          onSave={handleSaveWord}
        />
      )}
    </>
  );
}
