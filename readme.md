# Voice controlled Vehicle Project

In this project there will be a python code to recognize speech, process the
input and send desired data to Arduino platform via bluetooth link.

Check in your IDE that you have all the necessary libraries and packages installed.

## Components
- Raspberry Pi: The central computing unit responsible for processing commands and sensor data.
- Ultrasonic sensors: Used for detecting obstacles in the vehicle's path.
- Motor controllers: Control the movement of the vehicle's motors based on input commands.
- Camera module: Captures live video feed for remote monitoring.

## Getting started

### Setting up the Raspberry Pi
1. Hardware setup: Connect all necessary components to the Raspberry Pi according to the given diagrams.
2. Software installation:
    - Install the required libraries on your Raspberry Pi:
        ```pip install opencv-python tensorflow picamera```
### Running the project on Raspberry Pi
1. Clone the repository
   ```git clone <repository-url>```
2. Navigate to raspberry directory
   ```cd raspberry```
3. Run the main script: Execute the `main.py` script the initialize the vehicle
   ```python main.py```
4. Start the server: run 
```Mock serial port opened.
Recording dummy.wav...
Recording dummy.wav complete.
Simulating speech input. Recognizing...
Simulated speech recognized: turn on desktop the mountain
```

