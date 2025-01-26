import React from "react";

interface ProgressBarProps {
  progress: number;
  duration: number;
  onSeek: (value: number) => void;
}

export const ProgressBar = ({
  progress,
  duration,
  onSeek,
}: ProgressBarProps) => {
  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-full space-y-2">
      <input
        type="range"
        min="0"
        max={duration || 100}
        value={progress}
        onChange={(e) => onSeek(Number(e.target.value))}
        className="w-full"
      />
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>{formatTime(progress)}</span>
        <span>{formatTime(duration)}</span>
      </div>
    </div>
  );
};
