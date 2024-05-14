# Voice controlled Vehicle Project

This project contains a code to recognize speech using Google api, process
the data and send the desired data to remote controlled vehicle powered by
Raspberry Pi 5 board.

## Hardware Components
- Raspberry Pi: The central computing unit responsible for processing commands and sensor data. 
This project used model 5.
- Ultrasonic sensors: Used for detecting obstacles in the vehicle's path. In this project model was HC-SR04.
- Motor controllers: Control the movement of the vehicle's motors based on input commands. This project used L298N.
- Camera module: Captures live video feed for remote monitoring. This project used camera module 3.

## Software components
### Raspberry Pi
- _**Server**_: Responsible for opening a server to a HOST and PORT. Also responsible for handling 
the data received through the socket.
- **_Motor controller_**: Includes the functions to move the wheels through the L298N controller. 
Made by using the gpiozero framework and Robot library that includes inbuild moving functions.
- **_Command Handler_**: Has the functions to handle voice commands. All new voice commands should be
implemented into here.
- **_Video Stream_**: Handles the camera module. Uses libcamera functionality in Raspberry Pi to start and
stop the video feed. This is handled in a separate thread, so it does not interfere with the other running functions
in the project. Also this is responsible to send the video feed over the socket in real time.
- **_Main_**: The main file that starts the project when executed. All the functions should be running through the main
so there should be no need to separately start other services. Also the distance sensor is being handled in the main, using
distance_sensor_handler() function, that is constantly monitoring the distance in-front of the vehicle.

### Laptop
- **_Wifi Controller_**: Component for connecting, sending data and receiving data over the wifi network. In this project
wifi network was chosen to be the way to communicate and send data with Raspberry Pi, so this wifi controller handles this.
- **_Video Stream Recognition_**: Uses a MobileNetSSD model to recognize objects from the live video feed received from 
Raspberry Pi. Model vectors and configuration can be found in the **model** directory. It can be configured to use any 
video source, but this project uses the video source recorded from the Raspberry Pi.
- **_Stream Voice Recognition_**: Handles the voice recognition. It will listen the microphone, and when audio is detected
it sends the audio to google api. This then processed in the code and printed out.
- **_Control App_**: Responsible for running the laptop side of the project. It will execute the voice recognition and
passes the commands through the wifi_controller to Raspberry Pi.

## Features
- Remote control via server-client communication
- Autonomous navigation using ultrasonic sensor for obstacle detection and avoidance.
- Video streaming for real-time monitoring of the vehicle's surroundings.

## Getting started

### Networking the raspberry pi
You need to create a hotspot in the raspberry pi that you connect the laptop. This is done in the wifi
setting settings. Once you have created the hotspot in the raspberry pi you need to connect the laptop to 
that hotspot. Then you can run the control software successfully in the laptop and connect to raspberry. Note
that if this is not made, there is no way that the wifi_controller can connect the laptop to raspberry pi, it 
is not enough that they are in the same wifi network at this point. This maybe fixed in the future.

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

#### Running features separately
There are testing files for most of the features. For example if you want to test the autnonmous
movement, you can just execute ```python test_autonomous_movement.py```. This will start only the 
autonomous movement script, so that is possible to test. The ```robby.py``` is also ment for testing
the movements with a simple script.

### Running the control software on laptop
1. Clone the respository into laptop using the same `git clone ...` as before.
2. Navigate to speech_control directory
   ```cd speech_control```
3. Run the main script
    ```python control_app.py```



This `python main.py` start the main code execution and the server.


