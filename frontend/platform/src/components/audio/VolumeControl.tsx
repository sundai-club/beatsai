import React from "react";
import { Button } from "@/components/ui/button";
import { Volume2, VolumeX } from "lucide-react";

interface VolumeControlProps {
  volume: number;
  onVolumeChange: (value: number) => void;
  onMute: () => void;
  isMuted: boolean;
}

export const VolumeControl = ({
  volume,
  onVolumeChange,
  onMute,
  isMuted,
}: VolumeControlProps) => {
  return (
    <div className="flex items-center gap-2">
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
        className="w-24"
      />
    </div>
  );
};
