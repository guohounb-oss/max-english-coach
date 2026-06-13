"use client";

import { useState, useEffect, useRef } from "react";
import { Star, Bookmark, X, Loader2 } from "lucide-react";

interface WordPopupProps {
  word: string;
  x: number;
  y: number;
  onClose: () => void;
  onSave: (data: WordData) => void;
}

export interface WordData {
  word: string;
  chinese: string;
  pronunciation: string;
  example: string;
  example_cn: string;
}

export function WordPopup({ word, x, y, onClose, onSave }: WordPopupProps) {
  const [data, setData] = useState<WordData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/words/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word }),
    })
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [word]);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        onClose();
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [onClose]);

  // Position inside viewport
  const style: React.CSSProperties = {
    position: "fixed",
    left: Math.min(x, window.innerWidth - 280),
    top: Math.min(y, window.innerHeight - 250),
    zIndex: 100,
  };

  return (
    <div
      ref={ref}
      style={style}
      className="w-72 bg-card border border-border rounded-xl shadow-2xl p-4 animate-slide-up"
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-lg font-bold text-accent capitalize">{word}</span>
        <button onClick={onClose} className="text-muted-foreground hover:text-foreground">
          <X className="w-4 h-4" />
        </button>
      </div>

      {loading ? (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="w-4 h-4 animate-spin" />
          Translating...
        </div>
      ) : data ? (
        <div className="space-y-3 text-sm">
          {data.chinese && (
            <div>
              <span className="text-muted-foreground">中文：</span>
              <span>{data.chinese}</span>
            </div>
          )}
          {data.pronunciation && (
            <div>
              <span className="text-muted-foreground">音标：</span>
              <span className="font-mono text-accent">{data.pronunciation}</span>
            </div>
          )}
          {data.example && (
            <div>
              <span className="text-muted-foreground">例句：</span>
              <span className="italic">{data.example}</span>
              {data.example_cn && (
                <p className="text-xs text-muted-foreground mt-0.5">
                  {data.example_cn}
                </p>
              )}
            </div>
          )}

          <button
            onClick={() => {
              if (data && !saved) {
                onSave(data);
                setSaved(true);
              }
            }}
            disabled={saved}
            className={`w-full flex items-center justify-center gap-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              saved
                ? "bg-green-500/20 text-green-400"
                : "bg-accent/20 text-accent hover:bg-accent/30"
            }`}
          >
            {saved ? (
              <>✓ Saved</>
            ) : (
              <>
                <Bookmark className="w-3.5 h-3.5" />
                Save to Wordbook
              </>
            )}
          </button>
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">Translation unavailable</p>
      )}
    </div>
  );
}
