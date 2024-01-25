FROM python:3.9-alpine

WORKDIR /app

# Install required packages and debugging tools
RUN apk add --no-cache portaudio portaudio-dev alsa-utils alsa-lib build-base

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set the default audio input device for PyAudio
ENV AUDIODRIVER=alsa
ENV AUDIODEV=default

# Set environment variables for audio playback in PyAudio
ENV PYAUDIO_NO_ALSA_WRAPPER=1
ENV PYAUDIO_NO_PORTAUDIO_WRAPPER=1

CMD ["python", "main.py"]
