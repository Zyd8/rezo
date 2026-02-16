import whisper
import os

os.makedirs("models", exist_ok=True)

model = whisper.load_model("base", download_root="../models")
result = model.transcribe("../audio.wav", fp16=False)
print(result["text"])
