#-------Import Libraries----------------------------------
import time
import serial
import board
import busio
import digitalio
import adafruit_rfm9x
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import adafruit_gps
import pwmio
from adafruit_motor import servo
#--------Pins/Classes----------------------------------------------
# Radio
RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi= busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
btnA = digitalio.DigitalInOut(board.D5)
btnA.direction = digitalio.Direction.INPUT
btnA.pull = digitalio.Pull.UP
# GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False) 
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")
# Magnetometer/ Accelerometer
i2c = board.I2C()
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
# Servos
R_pwm= pwmio.PWMOut(board.D26,duty_cycle=2 ** 15, frequency=50)
L_pwm= pwmio.PWMOut(board.D20,duty_cycle=2 ** 15, frequency=50)
R_servo = servo.Servo(R_pwm)
L_servo = servo.Servo(L_pwm)
# Limit switches
Limit_Switch_Right= digitalio.DigitalInOut(board.D16)
Limit_Switch_Left= digitalio.DigitalInOut(board.D21)
Limit_Switch_Right.direction = digitalio.Direction.INPUT
Limit_Switch_Left.direction = digitalio.Direction.INPUT
Limit_Switch_Right.pull = digitalio.Pull.DOWN
Limit_Switch_Left.pull = digitalio.Pull.DOWN
#-------Variables------------------------------------------
# radio
data_recieved=0
data_sent=0
# Data sent from cansat
Accel_X = 0
Accel_Y = 0
Accel_Z = 0

Mag_X = 0
Mag_Y = 0
Mag_Z =0
Altt_offset=0
Altt_Value=0
Long_Value=0
Latt_Value=0
Num_Sat=0
gps_vel=0
gps_heading=0
gps_dilusion=0
rssi=0
# Slider Servo Pos 
Max_Glider_Pos=5
Min_Glider_Pos=-5
Current_Glider_R_Pos=0
Current_Glider_L_Pos=0
New_Glider_R_Pos=0
New_Glider_L_Pos=0
# Offsets
Accel_X_Offset_list = []
Accel_Y_Offset_list = []
Accel_Z_Offset_list = []
Mag_X_Offset_list = []
Mag_Y_Offset_list = []
Mag_Z_Offset_list =[]
Accel_X_Offset = 0
Accel_Y_Offset = 0
Accel_Z_Offset = 0
Mag_X_Offset = 0
Mag_Y_Offset = 0
Mag_Z_Offset =0
#----Classes-----------------------------------------


#----------------------------------------------------
def main():
    #------------------Boot up--------------------------------------------------------
    try:
        # Radio
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
        print('RFM9x: Detected')
    except RuntimeError as error:
        # Thrown on version mismatch
        print('RFM9x Error: ', error)
    Fix_Done=0
    last_print = time.monotonic()
    while Fix_Done==0:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
                last_print = current
                if not gps.has_fix:
                    print("Waiting for fix...")
                else:
                    print("fix found")
                    Fix_Done=1
    for i in range(10):
        Accel_X_Offset_list.append(accel.acceleration[0])
        Accel_Y_Offset_list.append(accel.acceleration[1])
        Accel_Z_Offset_list.append(accel.acceleration[2])
        Mag_X_Offset_list.append(mag.magnetic[0])
        Mag_Y_Offset_list.append(mag.magnetic[1])
        Mag_Z_Offset_list.append(mag.magnetic[2])
    Accel_X_Offset=sum(Accel_X_Offset_list)/len(Accel_X_Offset_list)
    Accel_Y_Offset=sum(Accel_Y_Offset_list)/len(Accel_Y_Offset_list)
    Accel_Z_Offset=sum(Accel_Z_Offset_list)/len(Accel_Z_Offset_list)
    Mag_X_Offset=sum(Mag_X_Offset_list)/len(Mag_X_Offset_list)
    Mag_Y_Offset=sum(Mag_Y_Offset_list)/len(Mag_Y_Offset_list)
    Mag_Z_Offset=sum(Mag_Z_Offset_list)/len(Mag_Z_Offset_list)

    New_Glider_R_Pos=0
    New_Glider_L_Pos=0
    while True:
        #print("Hello world")

        #Accelerometer data
        Accel_X=accel.acceleration[0]-Accel_X_Offset
        Accel_Y=accel.acceleration[1]-Accel_Y_Offset
        Accel_Z=accel.acceleration[2]-Accel_Z_Offset
        Mag_X=mag.magnetic[0]-Mag_X_Offset
        Mag_Y=mag.magnetic[1]-Mag_Y_Offset
        Mag_Z=mag.magnetic[2]-Mag_Z_Offset
        gps.update()
        Altt_Value=gps.altitude_m
        Long_Value=gps.longitude
        Latt_Value=gps.latitude
        Num_Sat=gps.satellites
        gps_vel=gps.speed_knots
        gps_heading=gps.track_angle_deg
        gps_dilusion=gps.horizontal_dilution
        data=[Accel_X,Accel_Y,Accel_Z,Mag_X,Mag_Y,Mag_Z,Altt_Value,Long_Value,Latt_Value,Num_Sat,gps_vel,gps_heading,gps_dilusion]
        data_sent=', '.join([str(elem) for elem in data])
        print(data_sent)
        
        data_recieved=rfm9x.receive()
        if data_recieved is not None:
            data_recieved_list=data_recieved.split(", ")
            New_Glider_R_Pos=data_recieved_list[0]
            New_Glider_L_Pos=data_recieved_list[1]
        if Current_Glider_R_Pos != New_Glider_R_Pos:
            if Current_Glider_R_Pos>New_Glider_R_Pos:
                print(" ")
                servo.angle = 0
                while not Limit_Switch_Right.value:
                    servo.angle = 0
            elif Current_Glider_R_Pos<New_Glider_R_Pos:
                print(" ")
                servo.angle = 180
                while not Limit_Switch_Right.value:
                    servo.angle = 180
        if Current_Glider_L_Pos !=New_Glider_L_Pos:
            if Current_Glider_L_Pos>New_Glider_L_Pos:
                print(" ")
                servo.angle = 0
                while not Limit_Switch_Right.value:
                    servo.angle = 0
            elif Current_Glider_L_Pos<New_Glider_L_Pos:
                print(" ")
                servo.angle = 180
                while not Limit_Switch_Right.value:
                    servo.angle = 180




    
    
if __name__ == "__main__":
    #BootUp()
    main()




