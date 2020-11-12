#!/usr/bin/env python
import os
import json
from time import sleep, time
import buttonshim
import picamera

version = "1.3"
run = True
camera = picamera.PiCamera()
camera.annotate_text_size = 100
buttonshim.set_pixel(0x00, 0x00, 0x00)
annotation_show_time = 4  #in seconds
button_hold_time = 2
annotation_off_time = 'null'
camera_settings_file = '/home/pi/camera_settings.txt'

def display_text(text):
    camera.annotate_text = text
    global annotation_off_time
    annotation_off_time = int(time()) + annotation_show_time

def display_settings():
    camera.annotate_background = picamera.Color('blue')
    annotation = 'version ' + version
    plain = True
    if camera.rotation > 0:
        plain = False
        annotation += '\n rotated '
    if camera.hflip:
        plain = False
        annotation += '\n horizontal flip '
    if camera.vflip:
        plain = False
        annotation += '\n vertical flip '
    if plain:
        annotation = '\n\n plain '
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

def save_settings():
    settings_file = open(camera_settings_file, 'r')
    settings = json.load(settings_file)
    settings_file.close()
    if (camera.rotation):
        settings['cam_rotation'] = True
    else:
        settings['cam_rotation'] = False
    if (camera.vflip):
        settings['cam_v_flip'] = True
    else:
        settings['cam_v_flip'] = False
    if (camera.hflip):
        settings['cam_h_flip'] = True
    else:
        settings['cam_h_flip'] = False
    settings_file = open(camera_settings_file, 'w')
    json.dump(settings, settings_file)
    settings_file.close()
        
def update_code():
    if os.path.exists('/media/pi') is False:
        display_text("\n\n no usb stick inserted ")
        return
    disk_names = os.listdir("/media/pi")
    if len(disk_names)==0:
        display_text("\n\n no usb stick inserted ")
        return
    #usb stick is present
    file_path = '/media/pi/' + disk_names[0] + '/update_code'
    if os.path.exists(file_path) and os.path.isfile(file_path):
        display_text("\n\n file found for updating ")
        sleep(2)
        if (check_for_same_version(file_path)):
            display_text('\n\n versions are the same \n no update needed ')
            return
        else:
            copy_code(file_path)
            display_text('\n\n code updated - rebooting ')
            sleep(2)
            camera.close()
            os.system('sudo shutdown -r now')
    else:
        display_text('\n\n no update file found on usb stick ')

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
        if camera.rotation:
            camera.rotation = 0
        else:
            camera.rotation = 180
        display_settings()
    elif button == 1:
        if camera.hflip:
            camera.hflip = False
        else:
            camera.hflip = True
        display_settings()
    elif button == 2:
        if camera.vflip:
            camera.vflip = False
        else:
            camera.vflip = True
        display_settings()
    elif button == 3:
        display_settings()
    elif button == 4:
        if camera.preview.fullscreen == True:
            camera.preview.window = (100, 100, int(1920/4), int(1080/4))
            camera.preview.fullscreen = False
        else:
            camera.preview.fullscreen = True

    save_settings()

@buttonshim.on_hold(buttonshim.BUTTON_A, hold_time = button_hold_time)
def holdA_handler(button):
    camera.vflip = False
    camera.hflip = False
    camera.rotation = 0
    save_settings()
    display_settings()
    
@buttonshim.on_hold(buttonshim.BUTTON_D, hold_time = button_hold_time)
def holdD_handler(button):
    update_code()

@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time = button_hold_time)
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
