from fastapi import FastAPI, Response
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import os
from io import BytesIO
from src.overlayer import overlay_wav_files

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()


@app.post("/get_beats/")
async def get_beats(text: str):
    """
    Convert text to speech and return a WAV file.

    :param text: The text to convert to speech
    :return: A WAV file containing the spoken text
    """


    wav_data = # Convert text to audio 

    return Response(content=wav_data, media_type="audio/wav")


@app.post("/get_soundtrack")
async def get_soundtrack(files: list[UploadFile] = File(...)):
    """
    Overlays multiple WAV files into one soundtrack.

    :param files: File uploads for the soundtrack of multiple WAV files
    :return: A WAV file containing the overlaid soundtrack
    """
    if len(files) == 0:
        return {"error": "No files uploaded."}

    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_paths.append(file_path)

    try:
        if len(file_paths) == 1:
            # Return the single file directly
            with open(file_paths[0], "rb") as f:
                output = BytesIO(f.read())
                output.seek(0)

            return StreamingResponse(
                output,
                media_type="audio/wav",
                headers={"Content-Disposition": f"attachment; filename={files[0].filename}"},
            )

        # Overlay multiple files
        combined_sound = overlay_wav_files(file_paths)
        output = BytesIO()
        combined_sound.export(output, format="wav")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=combined.wav"},
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Cleanup uploaded files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)