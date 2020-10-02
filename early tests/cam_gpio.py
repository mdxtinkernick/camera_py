from gpiozero import Button, OutputDevice
from picamera import PiCamera
from signal import pause
from time import sleep
import os

flip_camera_jumper = Button(21, pull_up = True)
stop_jumper = Button(16, pull_up = True, bounce_time = .1)
extra_earth = OutputDevice(19, initial_value=False)

def stop_camera():
    camera.stop_preview()
    exit()


camera = PiCamera()

camera.start_preview()

stop_jumper.when_released = stop_camera

count = 0
while count < 10:
    if flip_camera_jumper.is_pressed:
        if camera.rotation != 0:
            camera.rotation = 0
    else:
        if camera.rotation is 0:
            camera.rotation = 180
    sleep(1)


camera.stop_preview()
