from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
camera.vflip = True
sleep(10)
camera.vflip = False
sleep(10)
camera.stop_preview()
