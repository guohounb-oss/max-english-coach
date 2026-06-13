"use client";

import { useState, useEffect } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Star, Trash2, BookOpen, ArrowUpDown, X } from "lucide-react";

interface WordEntry {
  id: number;
  word: string;
  chinese: string;
  pronunciation: string;
  example: string;
  stars: number;
  created_at: string;
}

interface WordbookProps {
  onClose: () => void;
}

export function Wordbook({ onClose }: WordbookProps) {
  const [words, setWords] = useState<WordEntry[]>([]);
  const [sortBy, setSortBy] = useState<"time" | "star">("time");
  const [loading, setLoading] = useState(true);

  const fetchWords = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/words/saved/1?sort=${sortBy}`)
      .then((r) => r.json())
      .then((d) => {
        setWords(d.words || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchWords();
  }, [sortBy]);

  const handleStar = async (id: number, stars: number) => {
    await fetch(`http://localhost:8000/api/words/saved/${id}/star`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ stars }),
    });
    fetchWords();
  };

  const handleDelete = async (id: number) => {
    await fetch(`http://localhost:8000/api/words/saved/${id}`, {
      method: "DELETE",
    });
    fetchWords();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <Card className="w-full max-w-lg max-h-[85vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-accent" />
            <h2 className="text-lg font-semibold">Wordbook</h2>
            <span className="text-xs text-muted-foreground">
              ({words.length} words)
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() =>
                setSortBy(sortBy === "time" ? "star" : "time")
              }
              className={`flex items-center gap-1 text-xs px-2 py-1 rounded-lg transition-colors ${
                sortBy === "star"
                  ? "bg-accent/20 text-accent"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <ArrowUpDown className="w-3 h-3" />
              {sortBy === "time" ? "时间" : "星级"}
            </button>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {loading ? (
          <p className="text-center text-muted-foreground py-8">
            Loading...
          </p>
        ) : words.length === 0 ? (
          <div className="text-center py-8">
            <BookOpen className="w-10 h-10 text-muted-foreground mx-auto mb-2" />
            <p className="text-muted-foreground">
              单词本为空
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              在对话中点击单词 → Save to Wordbook
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {words.map((w) => (
              <div
                key={w.id}
                className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg hover:bg-secondary transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-accent capitalize">
                      {w.word}
                    </span>
                    {w.pronunciation && (
                      <span className="text-xs text-muted-foreground font-mono">
                        {w.pronunciation}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground truncate">
                    {w.chinese}
                  </p>
                  {w.example && (
                    <p className="text-xs text-muted-foreground italic truncate mt-0.5">
                      {w.example}
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-1 ml-2 shrink-0">
                  {[1, 2, 3, 4, 5].map((n) => (
                    <button
                      key={n}
                      onClick={() => handleStar(w.id, n)}
                      className="p-0.5"
                    >
                      <Star
                        className={`w-3.5 h-3.5 ${
                          n <= w.stars
                            ? "fill-yellow-400 text-yellow-400"
                            : "text-muted-foreground/40"
                        }`}
                      />
                    </button>
                  ))}
                  <button
                    onClick={() => handleDelete(w.id)}
                    className="p-1 text-muted-foreground hover:text-destructive transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
