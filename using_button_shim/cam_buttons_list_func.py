#!/usr/bin/env python
import json
import time
from signal import pause
import buttonshim
from picamera import PiCamera
import os

camera = PiCamera()

with open('camera_settings.txt') as settings_file:
    settings = json.load(settings_file)
    print(settings)
    if settings['cam_rotate']:
        camera.rotate = 180
    if settings['cam_h_flip']:
        camera.hflip = True
    if settings['cam_v_flip']:
        camera.vflip = True

@buttonshim.on_press([buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E])
def button(button, pressed):
    print(button_flag)
    if button == 0:
        settings['cam_rotate'] = not settings['cam_rotate']
        if settings['cam_rotate']:
            camera.rotate = 180
        else:
            camera.rotate = 0
    elif button == 1:
        settings['cam_h_flip'] = not settings['cam_h_flip']
        if settings['cam_h_flip']:
            camera.hflip = True
        else:
            camera.hflip = False
    elif button == 2:
        settings['cam_v_flip'] = not settings['cam_v_flip']
        if settings['cam_v_flip']:
            camera.vflip = True
        else:
            camera.vflip = False
    elif button == 3:
        pass
    elif button == 4:
        camera.stop_preview()
        exit()
    print(settings)
    with open('camera_settings.txt', 'w') as settings_file:
        json.dump(settings, settings_file)

camera.start_preview()

pause()

