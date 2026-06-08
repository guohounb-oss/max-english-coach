import { create } from "zustand";

export interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  audioB64?: string;
  corrections?: Correction[];
  vocabularySuggestions?: VocabularySuggestion[];
  timestamp: number;
}

export interface Correction {
  original: string;
  corrected: string;
  rule: string;
}

export interface VocabularySuggestion {
  weak_word: string;
  alternatives: string[];
}

export interface UserSettings {
  name: string;
  english_level: string;
  learning_mode: string;
  correction_frequency: string;
  voice_speed: number;
  voice_volume: number;
}

export interface DashboardStats {
  name: string;
  level: string;
  total_minutes: number;
  streak_days: number;
  vocabulary_learned: number;
  grammar_mistakes_corrected: number;
  total_conversations: number;
  fluency_trend: { date: string; score: number }[];
}

interface AppState {
  messages: Message[];
  isRecording: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
  settings: UserSettings;
  stats: DashboardStats | null;
  showSettings: boolean;
  showDashboard: boolean;

  addMessage: (msg: Message) => void;
  setRecording: (v: boolean) => void;
  setProcessing: (v: boolean) => void;
  setSpeaking: (v: boolean) => void;
  updateSettings: (s: Partial<UserSettings>) => void;
  setStats: (s: DashboardStats) => void;
  toggleSettings: () => void;
  toggleDashboard: () => void;
}

let msgCounter = 0;

export const useStore = create<AppState>((set) => ({
  messages: [],
  isRecording: false,
  isProcessing: false,
  isSpeaking: false,
  settings: {
    name: "Student",
    english_level: "intermediate",
    learning_mode: "free_conversation",
    correction_frequency: "moderate",
    voice_speed: 1.0,
    voice_volume: 1.0,
  },
  stats: null,
  showSettings: false,
  showDashboard: false,

  addMessage: (msg) =>
    set((s) => ({ messages: [...s.messages, { ...msg, id: `msg-${++msgCounter}` }] })),

  setRecording: (v) => set({ isRecording: v }),
  setProcessing: (v) => set({ isProcessing: v }),
  setSpeaking: (v) => set({ isSpeaking: v }),

  updateSettings: (partial) =>
    set((s) => ({ settings: { ...s.settings, ...partial } })),

  setStats: (stats) => set({ stats }),

  toggleSettings: () => set((s) => ({ showSettings: !s.showSettings, showDashboard: false })),
  toggleDashboard: () => set((s) => ({ showDashboard: !s.showDashboard, showSettings: false })),
}));
