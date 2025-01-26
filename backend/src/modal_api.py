from pathlib import Path
import modal
from typing import Optional

# Create Modal app
app = modal.App("musicgen-api")

# Set up image with dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg")
    .pip_install(
        "huggingface_hub[hf_transfer]==0.27.1",
        "torch==2.1.0",
        "numpy<2",
        "git+https://github.com/facebookresearch/audiocraft.git@v1.3.0"
    )
)

# Create cache volume for model weights
cache_dir = "/cache"
model_cache = modal.Volume.from_name("musicgen-model-cache", create_if_missing=True)

@app.cls(gpu="l40s", image=image, volumes={cache_dir: model_cache})
class MusicGenAPI:
    @modal.enter()
    def load_model(self):
        from audiocraft.models import MusicGen
        self.model = MusicGen.get_pretrained("facebook/musicgen-medium")
        self.sample_rate = self.model.sample_rate
        
    @modal.method()
    def generate_music(
        self,
        prompt: str,
        duration: int = 10,
        melody_path: Optional[str] = None
    ) -> bytes:
        """
        Generate music based on text prompt and optional melody.
        
        Args:
            prompt: Text description of desired music
            duration: Duration in seconds (max 30)
            melody_path: Optional path to melody audio file
        
        Returns:
            Generated audio as bytes
        """
        import torch
        import torchaudio
        from audiocraft.data.audio import audio_write_from_tensor
        
        # Set generation parameters
        self.model.set_generation_params(duration=min(duration, 30))
        
        if melody_path:
            melody, sr = torchaudio.load(melody_path)
            audio = self.model.generate_with_chroma(
                [prompt],
                melody[None].expand(1, -1, -1),
                sr
            )[0]
        else:
            audio = self.model.generate([prompt])[0]
            
        # Convert to audio bytes
        audio_path = f"/tmp/{prompt[:10]}.wav"
        audio_write_from_tensor(
            audio_path, 
            audio.cpu(),
            self.sample_rate,
            strategy="loudness",
            loudness_compressor=True
        )
        
        with open(audio_path, "rb") as f:
            return f.read()

@app.local_entrypoint()
def main():
    api = MusicGenAPI()
    # Example usage
    audio_bytes = api.generate_music.remote(
        prompt="Happy rock music with electric guitar",
        duration=10
    )
    
    # Save output
    output_path = Path("/tmp/output.wav")
    output_path.write_bytes(audio_bytes)
    print(f"Audio saved to {output_path}")
