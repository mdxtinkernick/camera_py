#!/usr/bin/env python
import json
import time
import signal
import buttonshim

with open('camera_settings.txt') as settings_file:
    settings = json.load(settings_file)

@buttonshim.on_press([buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E])
def button(button, pressed):
    global button_flag
    button_flag = button

button_flag = "null"

while True:
    time.sleep(.1)
    if (button_flag != "null"):
        print(button_flag)
        if button_flag == 0:
            settings['cam_rotate'] = not settings['cam_rotate']
        elif button_flag == 1:
            settings['cam_v_flip'] = not settings['cam_v_flip']
        elif button_flag == 2:
            settings['cam_v_flip'] = not settings['cam_v_flip']
        elif button_flag == 3:
            pass
        elif button_flag == 4:
            pass
        button_flag = button_flag = "null"
        print(settings)
        with open('camera_settings.txt', 'w') as settings_file:
            json.dump(settings, settings_file)
