"use client";

import { useStore } from "../../lib/store";
import { updateUser } from "../../lib/api";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { X } from "lucide-react";

const LEVELS = ["beginner", "elementary", "intermediate", "upper-intermediate", "advanced"];
const MODES = [
  // 对话模式
  { value: "free_conversation", label: "💬 Free Chat" },
  { value: "business_english", label: "💼 Business" },
  { value: "travel_english", label: "✈️ Travel" },
  { value: "interview_practice", label: "🎤 Interview" },
  { value: "american_slang", label: "🇺🇸 Slang" },
  { value: "pronunciation_practice", label: "🗣️ Pronunciation" },
  // 教学工具
  { value: "daily_course", label: "📅 Daily Course" },
  { value: "flashcards", label: "🃏 Flashcards" },
  { value: "grammar_decoder", label: "📖 Grammar Decoder" },
  { value: "quiz_assessment", label: "📝 Quiz" },
];
const FREQUENCIES = [
  { value: "low", label: "Low — Major errors only" },
  { value: "moderate", label: "Moderate — Natural flow" },
  { value: "high", label: "High — Correct everything" },
];

export function Settings() {
  const { settings, showSettings, toggleSettings, updateSettings } = useStore();

  if (!showSettings) return null;

  const handleChange = async (key: string, value: string | number | boolean) => {
    updateSettings({ [key]: value });
    try {
      await updateUser(1, { [key]: value });
    } catch (err) {
      console.error("Failed to save setting:", err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <Card className="w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Settings</h2>
          <Button variant="ghost" size="sm" onClick={toggleSettings}>
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="space-y-5">
          {/* Name */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              Your Name
            </label>
            <input
              type="text"
              value={settings.name}
              onChange={(e) => handleChange("name", e.target.value)}
              className="w-full bg-secondary border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-accent"
            />
          </div>

          {/* Level */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              English Level
            </label>
            <select
              value={settings.english_level}
              onChange={(e) => handleChange("english_level", e.target.value)}
              className="w-full bg-secondary border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-accent"
            >
              {LEVELS.map((l) => (
                <option key={l} value={l}>
                  {l.charAt(0).toUpperCase() + l.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Learning Mode */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              Learning Mode
            </label>
            <div className="grid grid-cols-2 gap-2">
              {MODES.map((m) => (
                <button
                  key={m.value}
                  onClick={() => handleChange("learning_mode", m.value)}
                  className={`text-xs px-3 py-2 rounded-lg border transition-colors text-left ${
                    settings.learning_mode === m.value
                      ? "border-accent bg-accent/20 text-accent"
                      : "border-border hover:bg-secondary"
                  }`}
                >
                  {m.label}
                </button>
              ))}
            </div>
          </div>

          {/* Correction Frequency */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              Correction Frequency
            </label>
            <div className="space-y-2">
              {FREQUENCIES.map((f) => (
                <button
                  key={f.value}
                  onClick={() => handleChange("correction_frequency", f.value)}
                  className={`w-full text-left text-xs px-3 py-2 rounded-lg border transition-colors ${
                    settings.correction_frequency === f.value
                      ? "border-accent bg-accent/20 text-accent"
                      : "border-border hover:bg-secondary"
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Voice Speed */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              Voice Speed: {settings.voice_speed}x
            </label>
            <input
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={settings.voice_speed}
              onChange={(e) =>
                handleChange("voice_speed", parseFloat(e.target.value))
              }
              className="w-full accent-accent"
            />
          </div>

          {/* Voice Volume */}
          <div>
            <label className="text-sm text-muted-foreground block mb-1">
              Voice Volume: {Math.round(settings.voice_volume * 100)}%
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={settings.voice_volume}
              onChange={(e) =>
                handleChange("voice_volume", parseFloat(e.target.value))
              }
              className="w-full accent-accent"
            />
          </div>
        </div>
      </Card>
    </div>
  );
}
