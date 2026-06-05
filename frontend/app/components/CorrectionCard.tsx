"use client";

import { Card } from "./ui/card";
import type { Correction } from "../../lib/store";
import { ArrowRight, Lightbulb } from "lucide-react";

interface CorrectionCardProps {
  corrections: Correction[];
}

export function CorrectionCard({ corrections }: CorrectionCardProps) {
  if (!corrections || corrections.length === 0) return null;

  return (
    <Card className="border-accent/30 bg-accent/5 animate-slide-up">
      <div className="flex items-center gap-2 mb-2">
        <Lightbulb className="w-4 h-4 text-accent" />
        <span className="text-xs font-medium text-accent">
          Quick Tip
        </span>
      </div>
      <div className="space-y-2">
        {corrections.map((c, i) => (
          <div key={i} className="text-sm">
            <div className="flex items-center gap-2 text-muted-foreground">
              <span className="line-through text-destructive/70">
                {c.original}
              </span>
              <ArrowRight className="w-3 h-3" />
              <span className="text-green-400 font-medium">
                {c.corrected}
              </span>
            </div>
            {c.rule && (
              <p className="text-xs text-muted-foreground mt-0.5 ml-1">
                {c.rule}
              </p>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
