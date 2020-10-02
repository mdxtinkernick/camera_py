from gpiozero import Button
from PiCamera import PiCamera
from signal import pause

button = Button(3, pull_up = False)
camera = PiCamera()

def button_released:
    camera.stop_preview()
    exit()
    
camera.start_preview()

button.when_released = button_released

pause()