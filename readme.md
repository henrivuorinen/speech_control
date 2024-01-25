#Python code to recognize speech

In this project there will be a python code to recognize speech, process the
input and send desired data to Arduino platform via bluetooth link.

## Running the project in Docker

To build and run the docker image excute

`docker build -t your-image-name .`

and

`docker run -it --rm --device=/dev/ttyUSB0:/dev/ttyUSB0 your-image-name`

Replace /dev/ttyUSB0 with the appropriate serial port of your Arduino. The --device flag is used to pass through the serial port to the Docker container.

