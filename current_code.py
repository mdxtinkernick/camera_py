#!/usr/bin/env python
import os
import json
from time import sleep, time
import buttonshim
import picamera

version = "1.2"
run = True
camera = picamera.PiCamera()
buttonshim.set_pixel(0x00, 0x00, 0x00)
annotation_show_time = 3  #in seconds
annotation_off_time = 'null'
camera_settings_file = '/home/pi/camera_settings.txt'

def display_text(text):
    camera.annotate_text = text
    global annotation_off_time
    annotation_off_time = int(time()) + annotation_show_time

def display_settings():
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
    display_text(annotation)

def extract_version(file_to_check):
    file = open(file_to_check)
    text = file.read()
    file.close()
    for item in text.split('\n'):
        if "version" in item:
            line = item.strip()
            break
    elements = line.split(' = ')
    version = elements[1].strip('"')
    return version

def check_for_same_version(file_path):
    return version == extract_version(file_path)

def copy_code(path_to_code):
    code_file = open(path_to_code)
    code = code_file.read()
    code_file.close()
    target_file = open(os.path.abspath(__file__), "w")
    target_file.write(code)
    target_file.close()

def update_code():
    disk_names = os.listdir("/media/pi")
    if os.path.exists('/media/pi') is False:
        display_text("no usb stick inserted")
        sleep(3)
        return
    disk_names = os.listdir("/media/pi")
    if len(disk_names)==0:
        display_text("no usb stick inserted")
        sleep(3)
        return
    #usb stick is present
    file_path = '/media/pi/' + disk_names[0] + '/update_code'
    if os.path.exists(file_path) and os.path.isfile(file_path):
        display_text("file found for updating")
        sleep(2)
        if (check_for_same_version(file_path)):
            display_text('versions are the same - no update needed')
            sleep(3)
            return
        else:
            copy_code(file_path)
            display_text('code updated - rebooting')
            sleep(2)
            camera.close()
            os.system('sudo shutdown -r now')
    else:
        display_text('no update file found on usb stick')

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
        text = 'version ' + version
        display_text(text)
    elif button == 4:
        if camera.preview.fullscreen == True:
            camera.preview.window = (100, 100, int(1920/4), int(1080/4))
            camera.preview.fullscreen = False
        else:
            camera.preview.fullscreen = True
    with open(camera_settings_file, 'w') as settings_file:
        json.dump(settings, settings_file)

@buttonshim.on_hold(buttonshim.BUTTON_D, hold_time = 2)
def holdD_handler(button):
    update_code()

@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time = 2)
def holdE_handler(button):
    camera.stop_preview()
    global run
    run = False

camera.start_preview()


while run:
    if annotation_off_time != 'null':
        if annotation_off_time < time():
            camera.annotate_text = ''
            annotation_off_time = 'null'
    sleep(1)

camera.close()
