# Import libraries
import RPi.GPIO as GPIO
import gps
import time
import board


# define Cansat
class CanSat(self):
    def __init__(self):# on start
        phase=1
        ServoPin1=
        ServoPin2=
        servo1Count=0
        servo2Count=0
        
    def UpdatePhase(self):
        if phase==1: # on ground
            
            phase=phase+1
        else if phase ==2:# in air
            
            phase=phase+1
        else if phase ==3: # falling

            phase=phase+1
        else if phase ==4: # Landed

            phase=phase+1

    def Check(self):# check gps,accel
        #accel data x y z
        # compass x y z
        # gps long latt altt

    def ReceiveData(self):

    def SendData(self):

    def MoveMotor(self, UserInfo):
        if phase==3: # motors can only move when falling

            if UserInfo == :

            else if UserInfo == :
            
            
            
            

        
