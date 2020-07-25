from gpiozero import Button, OutputDevice
from picamera import PiCamera
from signal import pause
from time import sleep
import os

stop_jumper = Button(5, pull_up = True, bounce_time = .1)
# first element in tuple is pin to be button, 
#second number, if zero then there is a ground pins opposite
#if more than 0 then that pins needs to be set low
jumper_pins[(21, 0), (20, 26), (16, 19), (13, 0), (6, 12)]
jumpers[]

for pins in jumper_pins:
    jumpers.apend(Button(pins[0], pull_up = True, bounce_time = .1))
    if pins[1] > 0:
        OutputDevice(pins[1], initial_value=False)


def stop_camera():
    camera.stop_preview()
    exit()


camera = PiCamera()

camera.start_preview()

stop_jumper.when_released = stop_camera

count = 0
while count < 30:
    #if jumper pin is present value would be default,
    #need to set it to default if not at it
    if jumper_pins[0].is_pressed:
        if camera.rotation is not 0:
            camera.rotation = 0
    else:
        #if it's at default value, need to set it to 
        #alternate value
        if camera.rotation is 0:
            camera.rotation = 180
            
    if jumper_pins[2].is_pressed:
        if camera.hflip is True:
            camera.hflip = False
    else:
        if camera.hflip is False:
            camera.hflip = True
            
    if jumper_pins[3].is_pressed:
        if camera.vflip is True:
            camera.vflip = False
    else:
        if camera.vflip is False:
            camera.vflip = True        
    sleep(1)

camera.stop_preview()
