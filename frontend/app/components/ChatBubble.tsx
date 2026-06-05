"use client";

import { cn } from "../../lib/utils";
import { Volume2 } from "lucide-react";

interface ChatBubbleProps {
  role: "user" | "assistant";
  text: string;
  isPlaying?: boolean;
}

export function ChatBubble({ role, text, isPlaying }: ChatBubbleProps) {
  const isUser = role === "user";

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
            <Volume2 className="w-4 h-4 animate-pulse text-accent" />
          )}
        </div>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-bold shrink-0">
          U
        </div>
      )}
    </div>
  );
}
