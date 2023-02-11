# IMPORT libraries
import time
import board
import busio
import adafruit_gps
import serial

# Initialize GPS class for GPS object in main.py
class GPS(self):
    def __init__(self):#on start
        #variables
        self.FixDone=0
        self.Long
        self.Latt
        #connect to serial
        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
        #create object from gps library
        self.gps = adafruit_gps.GPS(uart, debug=False)
        #turn on basic GGA and RMC info
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        #update rate is set to 1000 = 1Hz
        self.gps.send_command(b"PMTK220,1000")
        #used to print every second in rest of class
        self.last_print = time.monotonic()
    
    def StartFix(self):#make sure gps has a fix
        self.gps.update()
        while self.FixDone==0:
            self.current = time.monotonic()
            if self.current - self.last_print >= 1.0:
                self.last_print = self.current
                if not self.gps.has_fix:
                    print("Waiting for fix...")
                else:
                    print("fix found")
                    self.FixDone=1

    def GetLattAndLong(self):
        self.gps.update()
        
        return gps.latitude,gps.longitude
