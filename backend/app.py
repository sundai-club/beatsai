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

import logging

logging.basicConfig(level=logging.INFO)

openaiapi = OpenAIAPI()



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
async def get_soundtrack(files: list[UploadFile] = File(...)):
    """
    Overlays multiple WAV files into one soundtrack and returns it as base64-encoded audio data.

    :param files: File uploads for the soundtrack of multiple WAV files
    :return: JSON containing the sampling rate and base64-encoded audio data
    """
    if len(files) == 0:
        return JSONResponse(content={"error": "No files uploaded."}, status_code=400)

    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_paths.append(file_path)

    try:
        if len(file_paths) == 1:
            # Process the single file directly
            data, sample_rate = sf.read(file_paths[0])
        else:
            # Overlay multiple files
            combined_sound = overlay_wav_files(file_paths)

            # Export combined sound to a BytesIO buffer
            output = BytesIO()
            combined_sound.export(output, format="wav")
            output.seek(0)

            # Read the combined audio from the buffer
            data, sample_rate = sf.read(output)

        # Convert the audio data to base64
        audio_base64 = base64.b64encode(data.tobytes()).decode("utf-8")

        return {
            "sampling_rate": sample_rate,
            "audio": audio_base64,
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Cleanup uploaded files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000)