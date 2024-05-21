import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    if rec.AcceptWaveform(indata):
        print(json.loads(rec.Result()))
    else:
        print(json.loads(rec.PartialResult()))

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
    print("Listening...")
    sd.sleep(10000)
