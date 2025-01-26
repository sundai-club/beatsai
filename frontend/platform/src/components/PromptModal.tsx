"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";

interface PromptModalProps {
  isOpen: boolean;
  onClose: () => void;
  instrument: {
    id: string;
    name: string;
    icon: string;
    description: string;
    placeholder: string;
  } | null;
  onGenerate?: (track: {
    id: string;
    instrument: string;
    prompt: string;
    audioUrl: string;
  }) => void;
}

export default function PromptModal({
  isOpen,
  onClose,
  instrument,
  onGenerate,
}: PromptModalProps) {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      setIsLoading(true);
      // TODO: Replace with actual API call
      // For now, use demo audio files
      const demoAudio = `/demos/${instrument?.id}.mp3`;

      if (onGenerate) {
        onGenerate({
          id: `${instrument?.id}-${Date.now()}`,
          instrument: instrument?.name || "",
          prompt,
          audioUrl: demoAudio,
        });
      }

      onClose();
      setPrompt("");
    } catch (error) {
      console.error("Generation failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <span className="text-2xl">{instrument?.icon}</span>
            <DialogTitle>{instrument?.name}</DialogTitle>
          </div>
          <DialogDescription>{instrument?.description}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={instrument?.placeholder}
            className="min-h-[100px]"
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? "Generating..." : "Generate"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
