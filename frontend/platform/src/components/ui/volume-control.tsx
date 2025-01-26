import React from "react";
import { Button } from "@/components/ui/button";
import { Volume2, VolumeX } from "lucide-react";
import { cn } from "@/lib/utils";

interface VolumeControlProps {
  volume: number;
  onVolumeChange: (value: number) => void;
  onMute: () => void;
  isMuted: boolean;
  className?: string;
}

export function VolumeControl({
  volume,
  onVolumeChange,
  onMute,
  isMuted,
  className,
}: VolumeControlProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <Button variant="ghost" size="icon" onClick={onMute}>
        {isMuted ? (
          <VolumeX className="h-4 w-4" />
        ) : (
          <Volume2 className="h-4 w-4" />
        )}
      </Button>
      <input
        type="range"
        min="0"
        max="1"
        step="0.01"
        value={isMuted ? 0 : volume}
        onChange={(e) => onVolumeChange(Number(e.target.value))}
        className="w-24 h-2 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
      />
    </div>
  );
}
