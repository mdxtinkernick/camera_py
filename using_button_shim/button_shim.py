#!/usr/bin/env python
import json
from time import sleep, time
import buttonshim
import picamera

run =True
camera = picamera.PiCamera()
annotation_show_time = 3  #in seconds
annotation_off_time = 'null'
camera_settings_file = '/home/pi/camera_settings.txt'

def display_settings():
    global annotation_off_time
    camera.annotate_background = picamera.Color('blue')
    annotation = ' '
    if settings['cam_rotate']:
        annotation+='rotated '
    if settings['cam_h_flip']:
        annotation+='horizontally flipped '
    if settings['cam_v_flip']:
        annotation+='vertically flipped '
    if annotation == ' ':
        annotation = ' plain '
        camera.annotate_background = picamera.Color('green')
    camera.annotate_text = annotation
    annotation_off_time = int(time()) + annotation_show_time

with open(camera_settings_file) as settings_file:
    settings = json.load(settings_file)
    if settings['cam_rotate']:
        camera.rotation = 180
    if settings['cam_h_flip']:
        camera.hflip = True
    if settings['cam_v_flip']:
        camera.vflip = True
    display_settings()

@buttonshim.on_press([buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E])
def button(button, pressed):
    if button == 0:
        settings['cam_rotate'] = not settings['cam_rotate']
        if settings['cam_rotate']:
            camera.rotation = 180
        else:
            camera.rotation = 0
        display_settings()
    elif button == 1:
        settings['cam_h_flip'] = not settings['cam_h_flip']
        if settings['cam_h_flip']:
            camera.hflip = True
        else:
            camera.hflip = False
        display_settings()
    elif button == 2:
        settings['cam_v_flip'] = not settings['cam_v_flip']
        if settings['cam_v_flip']:
            camera.vflip = True
        else:
            camera.vflip = False
        display_settings()
    elif button == 3:
        pass
    elif button == 4:
        camera.stop_preview()
        global run
        run = False
    with open(camera_settings_file, 'w') as settings_file:
        json.dump(settings, settings_file)

camera.start_preview()

while run:
    if annotation_off_time != 'null':
        if annotation_off_time < time():
            camera.annotate_text = ''
            annotation_off_time = 'null'
    sleep(1)
