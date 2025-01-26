import os
from pydub import AudioSegment

def overlay_wav_files(file_paths):
    """Overlay multiple WAV files into one soundtrack."""
    combined = AudioSegment.from_file(file_paths[0])
    for file_path in file_paths[1:]:
        sound = AudioSegment.from_file(file_path)
        combined = combined.overlay(sound)
    return combined

file_paths = os.listdir("../demo_sounds")
file_paths = [os.path.join("../demo_sounds", file_path) for file_path in file_paths]
song = overlay_wav_files(file_paths)

song.export("output.wav", format="wav")