#!/usr/bin/env python
import json
import time
import signal
import buttonshim

with open('camera_settings.txt') as settings_file:
    settings = json.load(settings_file)

print settings['cam_rotate']

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global button_flag
    button_flag = "button_1"

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global button_flag
    button_flag = "button_2"

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global button_flag
    button_flag = "button_3"

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global button_flag
    button_flag = "button_4"

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    global button_flag
    button_flag = "button_5"

button_flag = "null"

while True:
    time.sleep(.1)
    if (button_flag != "null"):
        print(button_flag)
        if button_flag == "button_1":
            settings['cam_rotate'] = not settings['cam_rotate']
        elif button_flag == "button_2":
            settings['cam_v_flip'] = not settings['cam_v_flip']
        elif button_flag == "button_3":
            settings['cam_v_flip'] = not settings['cam_v_flip']
        elif button_flag == "button_4":
            pass
        elif button_flag == "button_5":
            pass
        button_flag = button_flag = "null"
        print(settings)
        with open('camera_settings.txt', 'w') as settings_file:
            json.dump(settings, settings_file)
