from picamera import PiCamera
from time import sleep
import cv2

camera = PiCamera()
count=0
while True:
    count+=1
    camera.start_recording('/home/pi/Desktop/Code/Recordings/Experiment/Vidio {}.h264'.format(count))
    sleep(120)
    camera.stop_recording()
    
