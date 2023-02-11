import board
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time 
import os
import sys
import AdapterBoard 
import cv2 as cv 
import numpy as np


Arducam_adapter_board = AdapterBoard.MultiAdapter()
i2c = board.I2C()
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)


if __name__ == "__main__":
    Arducam_adapter_board.init(320,240)
    #Arducam_adapter_board.select_channel("A")
    Arducam_adapter_board.preview()
    print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
    print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
