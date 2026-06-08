"use client";

import { useEffect, useRef } from "react";
import { useStore } from "../lib/store";
import { useVoiceChat } from "../hooks/useVoiceChat";
import { fetchUser } from "../lib/api";
import { MicrophoneButton } from "./components/MicrophoneButton";
import { ChatBubble } from "./components/ChatBubble";
import { CorrectionCard } from "./components/CorrectionCard";
import { VocabularyCard } from "./components/VocabularyCard";
import { Dashboard } from "./components/Dashboard";
import { Settings } from "./components/Settings";
import { Button } from "./components/ui/button";
import { BarChart3, Settings as SettingsIcon, MessageCircle } from "lucide-react";

export default function Home() {
  const {
    messages,
    updateSettings,
    toggleSettings,
    toggleDashboard,
    showSettings,
    showDashboard,
  } = useStore();

  const { isRecording, isProcessing, isSpeaking, pushToTalk, error } =
    useVoiceChat();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load user settings on mount
  useEffect(() => {
    fetchUser()
      .then((user) => {
        updateSettings({
          name: user.name,
          english_level: user.english_level,
          learning_mode: user.learning_mode,
          correction_frequency: user.correction_frequency,
          voice_speed: user.voice_speed,
          voice_volume: user.voice_volume,
        });
      })
      .catch(console.error);
  }, [updateSettings]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b border-border shrink-0">
        <div>
          <h1 className="text-lg font-semibold text-foreground">
            Max English Coach
          </h1>
          <p className="text-xs text-muted-foreground">
            Your witty AI English teacher
          </p>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="sm" onClick={toggleDashboard}>
            <BarChart3 className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleSettings}>
            <SettingsIcon className="w-4 h-4" />
          </Button>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <div className="w-20 h-20 rounded-full bg-secondary flex items-center justify-center">
              <MessageCircle className="w-10 h-10 text-muted-foreground" />
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-1">
                Ready to practice?
              </h2>
              <p className="text-sm text-muted-foreground max-w-sm">
                Press the mic button and start talking. I&apos;ll help you sound
                more natural — and maybe make you laugh along the way.
              </p>
            </div>
            {error && (
              <p className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">
                {error}
              </p>
            )}
          </div>
        )}

        {messages.map((msg, i) => {
          const prevCorrections = msg.corrections;
          const prevVocab = msg.vocabularySuggestions;

          return (
            <div key={msg.id} className="space-y-2">
              <ChatBubble
                role={msg.role}
                text={msg.text}
                audioB64={msg.audioB64}
                isPlaying={isSpeaking && i === messages.length - 1}
              />
              {prevCorrections && prevCorrections.length > 0 && (
                <CorrectionCard corrections={prevCorrections} />
              )}
              {prevVocab && prevVocab.length > 0 && (
                <VocabularyCard suggestions={prevVocab} />
              )}
            </div>
          );
        })}

        {isProcessing && (
          <div className="flex gap-3 animate-slide-up">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-xs font-bold">
              M
            </div>
            <div className="bg-secondary rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" />
                <span
                  className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                  style={{ animationDelay: "0.15s" }}
                />
                <span
                  className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                  style={{ animationDelay: "0.3s" }}
                />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      {/* Footer — Mic Button */}
      <footer className="shrink-0 border-t border-border px-4 py-4 flex justify-center bg-background">
        <MicrophoneButton
          isRecording={isRecording}
          isProcessing={isProcessing}
          onPushToTalk={pushToTalk}
        />
      </footer>

      {/* Modals */}
      <Dashboard />
      <Settings />
    </div>
  );
}
