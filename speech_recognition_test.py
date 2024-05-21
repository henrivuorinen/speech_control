import os
import json
import numpy as np
import pygame
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def initialize_audio():
    pygame.mixer.init()

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def play_error():
    play_sound(os.path.join("sounds", "error.wav"))

class SpeechRecognizer:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.initialized = False
        self.command = None

    def callback(self, indata, frames, time, status):
        if status:
            print("Status:", status, flush=True)
        data = np.frombuffer(indata, dtype=np.int16)  # Convert buffer to numpy array
        print("Data captured:", data)  # Debug print to check data capture
        if self.recognizer.AcceptWaveform(data.tobytes()):
            result = self.recognizer.Result()
            result_dict = json.loads(result)
            print("Result:", result_dict)  # Debug print to check the result
            if result_dict.get('text', ''):
                if not self.initialized:
                    if result_dict['text'] == "wake up":
                        play_sound(os.path.join("sounds", "start-test.wav"))
                        print("Wake word detected. Listening for commands")
                        self.initialized = True
                elif self.initialized:
                    self.command = result_dict['text']
                    print("Command detected:", self.command)
        else:
            partial_result = self.recognizer.PartialResult()
            print("Partial result:", partial_result)

    def listen_for_wake_word(self):
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.callback):
            print("Listening...")
            while True:
                if self.command:
                    yield self.command
                    self.command = None

if __name__ == "__main__":
    recognizer = SpeechRecognizer("vosk-model-small-en-us-0.15")
    initialize_audio()  # Initialize audio system

    for command in recognizer.listen_for_wake_word():
        if command == "move forward":
            # Your code to execute the "move forward" action
            print("Moving forward!")
            play_sound(os.path.join("sounds", "moving_forward.wav"))
        elif command == "shut down":
            print("Shutting down...")
            play_sound(os.path.join("sounds", "shut-down.wav"))
            break
