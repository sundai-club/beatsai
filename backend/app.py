from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import os
from io import BytesIO
from src.overlayer import overlay_wav_files
import requests
from src.openai_api import OpenAIAPI
import base64
import soundfile as sf
import numpy as np
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from typing import List

from fastapi import FastAPI, File, Form, UploadFile
import tempfile
import logging
from scipy.io.wavfile import write
logging.basicConfig(level=logging.INFO)

openaiapi = OpenAIAPI()
import json



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_beats/")
async def get_beats(request: dict):
    instrument = request['instrument']
    prompt = request['prompt']

    music_prompt = openaiapi.generate_audio_prompt(prompt, instrument)['prompt']
    logging.info("Generated music prompt: " + music_prompt)


    logging.info("Calling Modal API")
    audio_data = requests.post("https://mihir-athale01--beatsai-api-fastapi-app.modal.run/infer", json={'prompt': music_prompt}).json()
    logging.info("Received audio data")
    return audio_data


@app.post("/get_soundtrack")
async def combine_tracks(
    metadata: str = Form(...),
    audio_files: List[UploadFile] = File(...)
):
    try:
        # Parse metadata
        metadata = json.loads(metadata)
        print("Received metadata:", metadata)
        print(f"Received {len(audio_files)} audio files")

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Process each audio file
            processed_audio = []
            sample_rate = 44100

            for audio_file in audio_files:
                # Get track ID from filename
                file_id = audio_file.filename.split('_')[0]
                
                # Find corresponding metadata
                track_meta = next(
                    (m for m in metadata if m['track_id'] == file_id),
                    None
                )

                if not track_meta:
                    continue

                # Save temp file
                temp_path = os.path.join(temp_dir, audio_file.filename)
                with open(temp_path, "wb") as temp_file:
                    content = await audio_file.read()
                    temp_file.write(content)

                try:
                    # Load audio file
                    audio = AudioSegment.from_file(temp_path)

                    # Convert to mono
                    if audio.channels > 1:
                        audio = audio.set_channels(1)

                    # Set sample rate
                    if audio.frame_rate != sample_rate:
                        audio = audio.set_frame_rate(sample_rate)

                    # Apply volume (if not muted)
                    volume = track_meta['volume']
                    if volume > 0:
                        if volume != 1.0:
                            audio = audio.apply_gain(20 * np.log10(volume))
                    else:
                        continue  # Skip muted tracks

                    # Convert to numpy array
                    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
                    
                    samples = samples / np.iinfo(np.int16).max  # Normalize to [-1, 1]

                    processed_audio.append(samples)

                except Exception as e:
                    print(f"Error processing {audio_file.filename}: {str(e)}")
                    continue

            if not processed_audio:
                return JSONResponse(
                    status_code=422,
                    content={"error": "No valid audio tracks to combine"}
                )

            # Pad and combine tracks
            max_length = max(len(arr) for arr in processed_audio)
            padded_audio = [
                np.pad(arr, (0, max_length - len(arr)), 'constant')
                for arr in processed_audio
            ]

            # Mix tracks
            combined = np.sum(padded_audio, axis=0)

            # Normalize to prevent clipping
            if np.max(np.abs(combined)) > 1.0:
                combined = combined / np.max(np.abs(combined))

            # Convert to 16-bit PCM
            combined = (combined * np.iinfo(np.int16).max).astype(np.int16)

            # Write to WAV
            with io.BytesIO() as wav_io:
                sf.write(wav_io, combined, sample_rate, format='WAV')
                wav_io.seek(0)
                audio_data = wav_io.read()

            # Encode as base64
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')

            # Save the audio to a WAV file
            output_file = "output_audio.wav"
            write(output_file, sample_rate, combined)

            return {
                "audio": audio_b64,
                "sampling_rate": sample_rate
            }

    except Exception as e:
        print(f"Error combining tracks: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000)