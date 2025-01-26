import React from "react";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
  progress: number;
  duration: number;
  onSeek: (value: number) => void;
  className?: string;
}

export function ProgressBar({
  progress,
  duration,
  onSeek,
  className,
}: ProgressBarProps) {
  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className={cn("w-full space-y-2", className)}>
      <input
        type="range"
        min="0"
        max={duration || 100}
        value={progress}
        onChange={(e) => onSeek(Number(e.target.value))}
        className="w-full h-2 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
      />
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>{formatTime(progress)}</span>
        <span>{formatTime(duration)}</span>
      </div>
    </div>
  );
}
