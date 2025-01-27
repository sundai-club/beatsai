import os
import modal
from pathlib import Path
import os

MODEL_DIR = "/model"
DATA_DIR = "/data"

# Create Modal stub
app = modal.App(name="beatsai-api")

# Set up Modal image
image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "accelerate==0.31.0",
    "datasets~=2.13.0",
    "fastapi[standard]==0.115.4",
    "ftfy~=6.1.0",
    "huggingface-hub==0.26.2",
    "hf_transfer==0.1.8",
    "numpy<2",
    "peft==0.11.1",
    "pydantic==2.9.2",
    "sentencepiece>=0.1.91,!=0.1.92",
    "smart_open~=6.4.0",
    "starlette==0.41.2",
    "transformers~=4.41.2",
    "torch~=2.2.0",
    "triton~=2.2.0",
    "wandb==0.17.6",
    "python-multipart",
    "scipy"
)

# Configure image
image = (
    image.apt_install("git")
    .run_commands(
        "cd /root && git init .",
    )
)

# Set up volume and secrets
volume = modal.Volume.from_name("beatsai-model", create_if_missing=True)
data_volume = modal.Volume.from_name("beatsai-volume", create_if_missing=True)

image = image.env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})


@app.function(
    volumes={MODEL_DIR: volume, DATA_DIR: data_volume},
    image=image,
    timeout=1800,
)
def download_models(config):
    import torch
    from transformers import pipeline
    from huggingface_hub import snapshot_download

    snapshot_download(
        config.model_name,
        local_dir=MODEL_DIR,
        ignore_patterns=["*.pt", "*.bin"],
    )

    pipeline("text-to-audio", "facebook/musicgen-melody")

    torch.cuda.empty_cache()

@app.cls(image=image, gpu="A100", volumes={MODEL_DIR: volume, DATA_DIR: data_volume}, timeout=1800, keep_warm=1)
class Model:

    def __init__(self):
        import logging
        from transformers import pipeline
        self.pipe = pipeline("text-to-audio", "facebook/musicgen-melody", device='cuda')
        logging.info("Model loaded")


    @modal.method()
    def inference(self, prompt):
        import scipy
        import logging
        import base64
        import io
        import torch
        import os
        import datetime
        import time
        os.makedirs(os.path.join(DATA_DIR, 'generated_audio'), exist_ok=True)
        logging.info("Generating audio")

        urls = []
        with torch.no_grad():
            music_data = self.pipe(
                prompt,
                forward_params={"do_sample": True,}

            )

        sample_rate = music_data["sampling_rate"]
        audio = music_data["audio"]

        return {
            "sampling_rate": sample_rate,
            "audio": base64.b64encode(audio.tobytes()).decode("utf-8"),
        }
        