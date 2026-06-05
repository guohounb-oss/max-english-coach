"use client";

import { useEffect } from "react";
import { useStore, type DashboardStats } from "../../lib/store";
import { fetchStats } from "../../lib/api";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import {
  TrendingUp,
  BookOpen,
  Clock,
  Flame,
  MessageCircle,
  CheckCircle2,
  X,
} from "lucide-react";

export function Dashboard() {
  const { stats, setStats, showDashboard, toggleDashboard } = useStore();

  useEffect(() => {
    if (showDashboard) {
      fetchStats().then(setStats).catch(console.error);
    }
  }, [showDashboard, setStats]);

  if (!showDashboard) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <Card className="w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Your Progress</h2>
          <Button variant="ghost" size="sm" onClick={toggleDashboard}>
            <X className="w-4 h-4" />
          </Button>
        </div>

        {stats ? (
          <div className="space-y-4">
            {/* Stats grid */}
            <div className="grid grid-cols-2 gap-3">
              <StatBadge
                icon={<Clock className="w-4 h-4" />}
                label="Minutes"
                value={String(stats.total_minutes)}
              />
              <StatBadge
                icon={<Flame className="w-4 h-4" />}
                label="Day Streak"
                value={String(stats.streak_days)}
              />
              <StatBadge
                icon={<BookOpen className="w-4 h-4" />}
                label="Words"
                value={String(stats.vocabulary_learned)}
              />
              <StatBadge
                icon={<CheckCircle2 className="w-4 h-4" />}
                label="Fixed"
                value={String(stats.grammar_mistakes_corrected)}
              />
            </div>

            {/* Level */}
            <div className="text-center p-3 bg-secondary rounded-lg">
              <p className="text-sm text-muted-foreground">Level</p>
              <p className="text-xl font-bold capitalize">{stats.level}</p>
            </div>

            {/* Fluency trend simple bar */}
            {stats.fluency_trend.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-accent" />
                  <span className="text-sm text-muted-foreground">
                    Fluency Trend
                  </span>
                </div>
                <div className="flex items-end gap-1 h-20">
                  {stats.fluency_trend.slice(-14).map((point, i) => (
                    <div
                      key={i}
                      className="flex-1 bg-accent/60 rounded-t"
                      style={{ height: `${Math.max(4, point.score)}%` }}
                      title={`${point.date}: ${point.score}`}
                    />
                  ))}
                </div>
              </div>
            )}

            <p className="text-xs text-center text-muted-foreground">
              {stats.total_conversations} conversations total
            </p>
          </div>
        ) : (
          <p className="text-center text-muted-foreground py-8">
            Loading stats...
          </p>
        )}
      </Card>
    </div>
  );
}

function StatBadge({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center gap-3 p-3 bg-secondary rounded-lg">
      <div className="text-accent">{icon}</div>
      <div>
        <p className="text-lg font-bold">{value}</p>
        <p className="text-xs text-muted-foreground">{label}</p>
      </div>
    </div>
  );
}
