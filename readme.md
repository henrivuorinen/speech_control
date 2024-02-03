#Python code to recognize speech

In this project there will be a python code to recognize speech, process the
input and send desired data to Arduino platform via bluetooth link.

Check in your IDE that you have all the necessary libraries and packages installed.

## Running without Docker

You need to install flac if you use macbook, that is easily done via homebrew `brew install flac`

Go into the main directory and run `python3 main.py`. This shoud start the main.py. When using the MockSerial for mocking the bluetooth connection, you should see output something like this:

```Mock serial port opened.
Recording dummy.wav...
Recording dummy.wav complete.
Simulating speech input. Recognizing...
Simulated speech recognized: turn on desktop the mountain
```

## Running the project in Docker

To build and run the docker image excute

`docker build -t your-image-name .`

and

`docker run -it --rm --device=/dev/ttyUSB0:/dev/ttyUSB0 your-image-name`

Replace /dev/ttyUSB0 with the appropriate serial port of your Arduino. The --device flag is used to pass through the serial port to the Docker container.

