from gpiozero import Robot, Motor

from time import sleep

robby = Robot(left=Motor(9, 10), right=Motor(7, 8))

for i in range(4):
    robby.forward()
    sleep(2)
    robby.backward()
    sleep(1)
    robby.right()
    sleep(0.4)
    robby.stop()