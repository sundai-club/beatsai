import requests
import base64
import numpy as np
from scipy.io.wavfile import write

prompt = "happy rock music with electric guitar"
audio_data = requests.post("https://mihir-athale01--beatsai-api-fastapi-app.modal.run/infer", json={'prompt': prompt}).json()

audio_bytes = base64.b64decode(audio_data["audio"])

# Convert bytes back to numpy array (assuming 16-bit PCM)
audio_array = np.frombuffer(audio_bytes, dtype=np.float32)

# Save the audio to a WAV file
output_file = "output_audio.wav"
write(output_file, audio_data["sampling_rate"], audio_array)
