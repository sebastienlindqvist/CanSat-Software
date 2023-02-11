import board
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time 
#import os
#import sys

i2c = board.I2C()
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
while True:
    #sys.stdout.write("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
    #print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
    #print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
    print(accel.acceleration[0])
    #clear = lambda: os.system("clear")
    time.sleep(1)
    #sys.stdout.flush()
    
