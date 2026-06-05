import { cn } from "../../../lib/utils";

interface CardProps {
  className?: string;
  children: React.ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card p-4",
        className
      )}
    >
      {children}
    </div>
  );
}
