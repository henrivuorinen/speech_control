from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(23, 24)

while True:
    print("Distance is: ", sensor.distance, "m")
    sleep(1)