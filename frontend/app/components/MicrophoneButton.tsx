"use client";

import { Mic, MicOff, Loader2 } from "lucide-react";
import { cn } from "../../lib/utils";

interface MicrophoneButtonProps {
  isRecording: boolean;
  isProcessing: boolean;
  onPushToTalk: () => void;
}

export function MicrophoneButton({
  isRecording,
  isProcessing,
  onPushToTalk,
}: MicrophoneButtonProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <button
        onClick={onPushToTalk}
        disabled={isProcessing}
        className={cn(
          "w-16 h-16 rounded-full flex items-center justify-center transition-all",
          "bg-primary text-primary-foreground hover:bg-primary/90",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          isRecording && "mic-recording bg-destructive hover:bg-destructive/90"
        )}
        aria-label={isRecording ? "Stop recording" : "Start recording"}
      >
        {isProcessing ? (
          <Loader2 className="w-7 h-7 animate-spin" />
        ) : isRecording ? (
          <MicOff className="w-7 h-7" />
        ) : (
          <Mic className="w-7 h-7" />
        )}
      </button>
      <span className="text-xs text-muted-foreground">
        {isProcessing
          ? "Processing..."
          : isRecording
          ? "Tap to stop"
          : "Push to talk"}
      </span>
    </div>
  );
}
