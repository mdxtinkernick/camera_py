import json

with open('camera_settings.txt') as settings_file:
    settings = json.load(settings_file)

print settings['cam_rotate']

settings['cam_rotate'] = True

with open('camera_settings.txt', 'w') as settings_file:
    json.dump(settings, settings_file)