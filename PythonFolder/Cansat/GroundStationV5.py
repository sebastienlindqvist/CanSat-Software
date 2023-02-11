#------Importing Libraries--------------------------------------------------------------
#region
from tkinter import *
from PIL import Image, ImageTk
from PIL import *
import math
import time
import numpy as np
import board
import busio
import digitalio
import adafruit_rfm9x
#import adafruit_rfm9x
#endregion
#-----------Setting up variables---------------------------------------------------------
#region

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
Altt_Value=0
Long_Value=0
Latt_Value=0
Num_Sat=0
gps_vel=0
gps_heading=0
phase=0
rssi=0
# Slider Servo Pos 
Max_Glider_Pos=5
Min_Glider_Pos=-5
Current_Glider_R_Pos=0
Current_Glider_L_Pos=0
# Calculations
last_time=time.time()
Current_Latt=0
Current_long=0
Current_Vel_X=1
Current_Vel_Y=1
Current_Vel_Z=1
Vertical_Vel=Current_Vel_Z
Horizontal_Vel=math.sqrt((Current_Vel_X^2)+(Current_Vel_Y^2))
Abs_Vel=math.sqrt((Current_Vel_X^2)+(Current_Vel_Y^2)+(Current_Vel_Z^2))
angle=0
Compass_angle=0
Current_Compass_angle=0
ETA_Num=Altt_Value/Vertical_Vel
#endregion
#------------------Create GUI Window---------------------------------------------------------------------
#region
window = Tk()
window.title("CanSat Trajectory")
window.geometry("1920x1800")
#----------------Create Frame for pilot info-------------------------------------------------------------
frame=Frame(window, borderwidth=5, relief="ridge", width=300, height=700)
#------------------Create Canvas'------------------------------------------------------------------------
SliderCanvas=Canvas(window, width=300,height=500)
CompassCanvas= Canvas(window, width=1500,height=40)# Canvas for compass on top
my_canvas = Canvas(window, width=1500,height=900)#Canvas with google image
my_canvas.grid(row=1,column=0, rowspan=6)#place google map below compass
CompassCanvas.grid(row=0,column=0)#Place compass canvas on top
frame.grid(row=0,column=1, rowspan=3,sticky="n")#place frame right of google maps
SliderCanvas.grid(row=4,column=1)

#--------Import Images---------------------------------------------------------------------------------
Google_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/map.png')
PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
Compass_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Compass.png')
CompassCentre_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/CompassCentre.png')
Slider_Background_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Slider Background.png')
Slider_Slider_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Paraglider_Bar.png')

#---------Place Images Inside Canvas'--------------------------------------------------------------------
GoogleMap=my_canvas.create_image(750,450,image=Google_Image, anchor='center')
Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")
Compass_Centre=CompassCanvas.create_image(750,40,image=CompassCentre_Image)
Compass=CompassCanvas.create_image(750,20,image=Compass_Image)
Slider_Background=SliderCanvas.create_image(0,0,image=Slider_Background_Image,anchor='nw')
Slider_Slider_1=SliderCanvas.create_image(43,240,image=Slider_Slider_Image, anchor='center')
Slider_Slider_2=SliderCanvas.create_image(129,240,image=Slider_Slider_Image, anchor='center')
#endregion
#---------------------------------------------------------------------------------------------------------
def move_up(event):
    my_canvas.move(GoogleMap,0,+5)
def move_down(event):
    my_canvas.move(GoogleMap,0,-5)
def move_left(event):
    my_canvas.move(GoogleMap,+5,0)
def move_right(event):
    my_canvas.move(GoogleMap,-5,0)

def Update_map():
    Pixel_Degree_Ratio=0 #
    if Current_Latt != Latt_Value or Current_long != Long_Value:
        Long_move_pixel=(Current_long-Long_Value)*Pixel_Degree_Ratio
        Latt_move_pixel=(Current_Latt-Latt_Value)*Pixel_Degree_Ratio
        my_canvas.move(GoogleMap,Long_move_pixel,Latt_move_pixel)
#-----------------------------------------------------------------------------------
def Compass_move_left(event):
    global angle
    angle=angle-0.97
    my_canvas.delete("Cansat_Arrow")
    PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    PIL_Cansat_Image=PIL_Cansat_Image.rotate(angle)
    #PIL_Cansat_Image.save('C:/Users/sebastien/Downloads/Cansat_Arrow.png')
    Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
    Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")
    
    CompassCanvas.move(Compass,-5,0)
    if CompassCanvas.coords(Compass)[0] <= -25:
        CompassCanvas.move(Compass,+1855,0)
    Cansat_Arrow.update()
    
def Compass_move_right(event):
    global angle
    angle=angle+0.97
    my_canvas.delete("Cansat_Arrow")
    PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    PIL_Cansat_Image=PIL_Cansat_Image.rotate(angle)
    Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
    Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")

    
    CompassCanvas.move(Compass,+5,0)
    if CompassCanvas.coords(Compass)[0] >= 1830:
        CompassCanvas.move(Compass,-1855,0)

    Cansat_Arrow.update()

def Update_Arrow_Compass():
    Pixel_Angle_ratio=0
    Angle_Change=(Compass_angle-Current_Compass_angle)*Pixel_Angle_ratio
    if Current_Compass_angle != Compass_angle:
        CompassCanvas.move(Compass,Angle_Change,0)
        if CompassCanvas.coords(Compass)[0] <= -25:
            CompassCanvas.move(Compass,+1855,0)

        elif CompassCanvas.coords(Compass)[0] >= 1830:
            CompassCanvas.move(Compass,-1855,0)
#----------------------------------------------------------------------------------------------
def Move_Left_Slider_Up(event):
    global Current_Glider_L_Pos
    if Current_Glider_L_Pos<Max_Glider_Pos:
        SliderCanvas.move(Slider_Slider_1,0,-44)
        Current_Glider_L_Pos=Current_Glider_L_Pos+1
def Move_Left_Slider_Down(event):
    global Current_Glider_L_Pos
    if Current_Glider_L_Pos>Min_Glider_Pos:
        SliderCanvas.move(Slider_Slider_1,0,+44)
        Current_Glider_L_Pos=Current_Glider_L_Pos-1
def Move_Right_Slider_Up(event):
    global Current_Glider_R_Pos
    if Current_Glider_R_Pos<Max_Glider_Pos:
        SliderCanvas.move(Slider_Slider_2,0,-44)
        Current_Glider_R_Pos=Current_Glider_R_Pos+1
def Move_Right_Slider_Down(event):
    global Current_Glider_R_Pos
    if Current_Glider_R_Pos>Min_Glider_Pos:
        SliderCanvas.move(Slider_Slider_2,0,+44)
        Current_Glider_R_Pos=Current_Glider_R_Pos-1
#------------------Bind Keys----------------------------------------------------------------
#region
window.bind("<w>",move_up)
window.bind("<s>",move_down)
window.bind("<a>",move_left)
window.bind("<d>",move_right)

window.bind("<e>",Compass_move_left)
window.bind("<q>",Compass_move_right)

window.bind("<i>",Move_Left_Slider_Up)
window.bind("<j>",Move_Left_Slider_Down)
window.bind("<o>",Move_Right_Slider_Up)
window.bind("<k>",Move_Right_Slider_Down)

#endregion
#-----------Creating Labels and Others---------------------------------------------------------------------------------
def Update_Vel(last_time):
    global Current_Vel_X
    global Current_Vel_Y
    global Current_Vel_Z
    current_time=time.time()
    Current_Vel_X=Current_Vel_X+Accel_X*(current_time-last_time)
    Current_Vel_Y=Current_Vel_Y+Accel_Y*(current_time-last_time)
    Current_Vel_Z=Current_Vel_Z+Accel_Z*(current_time-last_time)
    last_time=current_time
    


Altt = Label(frame,text="Altt: ",font=("font",25)).grid(row=0,column=1)
AlttNum = Label(frame,text=Altt_Value,font=("font",25)).grid(row=0,column=2)
Long = Label(frame,text="Long: ",font=("font",25)).grid(row=1,column=0)
LongNum = Label(frame,text=Long_Value,font=("font",25)).grid(row=1,column=1)
Latt = Label(frame,text="Latt: ",font=("font",25)).grid(row=1,column=2)
LattNum = Label(frame,text=Latt_Value,font=("font",25)).grid(row=1,column=3)

H_Vel = Label(frame,text="H. Vel: ",font=("font",25)).grid(row=2,column=0)
H_Vel_Num = Label(frame,text=round(Horizontal_Vel,2),font=("font",25)).grid(row=2,column=1)

V_Vel = Label(frame,text="V. Vel: ",font=("font",25)).grid(row=2,column=2)
V_Vel_Num = Label(frame,text=round(Vertical_Vel,2),font=("font",25)).grid(row=2,column=3)

Vel_abs = Label(frame,text="Mag. V:",font=("font",25)).grid(row=3,column=1) 
Vel_abs_num = Label(frame,text=round(Abs_Vel,2),font=("font",25)).grid(row=3,column=2) 

Eta = Label(frame,text="ETA: ",font=("font",25)).grid(row=4,column=0)
Eta_Num = Label(frame,text=ETA_Num,font=("font",25)).grid(row=4,column=1)

#---------Place Inside Grid----------------------------------------------------------------------------------------






#
#my_canvas.itemconfig(Cansat_Arrow,image=Cansat_Image)

RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi= busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
btnA = digitalio.DigitalInOut(board.D5)
btnA.direction = digitalio.Direction.INPUT
btnA.pull = digitalio.Pull.UP

try:
    # Radio
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
    print('RFM9x: Detected')
except RuntimeError as error:
    print('RFM9x Error: ', error)
window.mainloop()
while True:
    data_recieved=rfm9x.receive()
    #PIL_Cansat_Image=Image.open('C:/Users/sebastien/Downloads/Cansat_Arrow.png')
    #global Cansat_Image
    #Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
    #my_canvas.itemconfig(Cansat_Arrow,image=Cansat_Image)
    #Cansat_Arrow.update()
    #window.update()
