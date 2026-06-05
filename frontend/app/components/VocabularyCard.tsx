"use client";

import { Card } from "./ui/card";
import type { VocabularySuggestion } from "../../lib/store";
import { Sparkles } from "lucide-react";

interface VocabularyCardProps {
  suggestions: VocabularySuggestion[];
}

export function VocabularyCard({ suggestions }: VocabularyCardProps) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <Card className="border-green-500/20 bg-green-500/5 animate-slide-up">
      <div className="flex items-center gap-2 mb-2">
        <Sparkles className="w-4 h-4 text-green-400" />
        <span className="text-xs font-medium text-green-400">
          Try Saying
        </span>
      </div>
      <div className="space-y-2">
        {suggestions.map((s, i) => (
          <div key={i} className="text-sm">
            <span className="text-muted-foreground line-through">
              {s.weak_word}
            </span>
            <span className="text-muted-foreground"> → </span>
            <span className="text-green-300 font-medium">
              {s.alternatives?.join(", ")}
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
}
