# camera_py

code for making pi and pi camera hq into an hdmi camera. Uses pimoroni button shim to provide buttons.

sd card image is available that autoruns the code on boot

Press button:

 R rotates the image 180
 
 H flips the images horizontally
 
 V flips the image vertically
 
 U displays the current settings without changing anything
 
 W toggles between full screen and windowed display from camera
 
 Holding button down:
 
 R resets display straigh from camera, without any flip or rotation
 
 U attempts to update code - looks for usb stick connected with file named update_code which has the new code in it.
 
 W quits the prgoram and returns to pi desktop
