import speech_recognition as sr
import pyaudio
import wave

from bluetooth import BluetoothController

def record_audio(filename="dummy.wav", duration=5):
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print(f"Recording {filename}...")

    frames = []
    for _ in range(0, int(44100 / 1024 * duration)):
        frames.append(stream.read(1024))

    print(f"Recording {filename} complete.")

    # Stop and close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech():
    recognizer = sr.Recognizer()

    # Record audio
    record_audio()

    with sr.AudioFile("dummy.wav") as source:
        print("Simulating speech input. Recognizing...")
        audio = recognizer.record(source)

    try:
        command = recognizer.recognize_google(audio, language='fi-FI').lower()
        print("Simulated speech recognized:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand simulated speech.")
        return None
    except sr.RequestError as e:
        print(f"Error making the request; {e}")
        return None

def run_voice_control():
    arduino_port = 'mock'
    bluetooth_controller = BluetoothController(port=arduino_port)

    while True:
        command = recognize_speech()
        if command:
            bluetooth_controller.send_data(command)

if __name__ == "__main__":
    run_voice_control()
