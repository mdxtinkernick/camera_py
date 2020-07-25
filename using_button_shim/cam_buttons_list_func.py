#!/usr/bin/env python
import json
import time
from signal import pause
import buttonshim

with open('camera_settings.txt') as settings_file:
    settings = json.load(settings_file)
    print(settings)

@buttonshim.on_press([buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E])
def button(button, pressed):
    print(button_flag)
    if button == 0:
        settings['cam_rotate'] = not settings['cam_rotate']
    elif button == 1:
        settings['cam_h_flip'] = not settings['cam_h_flip']
    elif button == 2:
        settings['cam_v_flip'] = not settings['cam_v_flip']
    elif button == 3:
        pass
    elif button == 4:
        exit()
    print(settings)
    with open('camera_settings.txt', 'w') as settings_file:
        json.dump(settings, settings_file)

pause()

