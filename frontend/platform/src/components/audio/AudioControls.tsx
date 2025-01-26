import React from "react";
import { Button } from "@/components/ui/button";
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Repeat,
  Shuffle,
} from "lucide-react";

interface AudioControlsProps {
  isPlaying: boolean;
  onPlayPauseClick: () => void;
  onPrevClick: () => void;
  onNextClick: () => void;
  onRepeatClick: () => void;
  onShuffleClick: () => void;
  isRepeat: boolean;
  isShuffle: boolean;
}

export const AudioControls = ({
  isPlaying,
  onPlayPauseClick,
  onPrevClick,
  onNextClick,
  onRepeatClick,
  onShuffleClick,
  isRepeat,
  isShuffle,
}: AudioControlsProps) => {
  return (
    <div className="flex items-center justify-center gap-4">
      <Button variant="ghost" size="icon" onClick={onShuffleClick}>
        <Shuffle
          className={`h-4 w-4 ${
            isShuffle ? "text-primary" : "text-muted-foreground"
          }`}
        />
      </Button>
      <Button variant="ghost" size="icon" onClick={onPrevClick}>
        <SkipBack className="h-4 w-4" />
      </Button>
      <Button size="icon" onClick={onPlayPauseClick}>
        {isPlaying ? (
          <Pause className="h-4 w-4" />
        ) : (
          <Play className="h-4 w-4" />
        )}
      </Button>
      <Button variant="ghost" size="icon" onClick={onNextClick}>
        <SkipForward className="h-4 w-4" />
      </Button>
      <Button variant="ghost" size="icon" onClick={onRepeatClick}>
        <Repeat
          className={`h-4 w-4 ${
            isRepeat ? "text-primary" : "text-muted-foreground"
          }`}
        />
      </Button>
    </div>
  );
};
