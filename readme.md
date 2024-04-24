# Voice controlled Vehicle Project

In this project there will be a python code to recognize speech, process the
input and send desired data to Arduino platform via bluetooth link.

Check in your IDE that you have all the necessary libraries and packages installed.

## Components
- Raspberry Pi: The central computing unit responsible for processing commands and sensor data.
- Ultrasonic sensors: Used for detecting obstacles in the vehicle's path.
- Motor controllers: Control the movement of the vehicle's motors based on input commands.
- Camera module: Captures live video feed for remote monitoring.

## Features
- Remote control via server-client communication
- Autonomous navigation using ultrasonic sensor for obstacle detection and avoidance.
- Video streaming for real-time monitoring of the vehicle's surroundings.

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

### Running the control software on laptop
1. Clone the respository into laptop using the same `git clone ...` as before.
2. Navigate to speech_control directory
   ```cd speech_control```
3. Run the main script
    ```python control_appgit .py```


This `python main.py` start the main code execution and the server.


