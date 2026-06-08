"use client";

import { cn } from "../../lib/utils";
import { playAudioFromBase64 } from "../../lib/audio";
import { Volume2, RotateCcw } from "lucide-react";
import { useState } from "react";

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

  return (
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
          <span>{text}</span>
          {isPlaying && (
            <Volume2 className="w-4 h-4 animate-pulse text-accent shrink-0" />
          )}
        </div>
      </div>

      {/* Replay button for AI messages */}
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
  );
}
