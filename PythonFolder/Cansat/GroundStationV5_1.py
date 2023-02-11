#------Importing Libraries--------------------------------------------------------------
#region
from tkinter import *
from PIL import Image, ImageTk
from PIL import *
import math
import time
import numpy as np


#import adafruit_rfm9x
#endregion
#-----------Setting up variables---------------------------------------------------------
#region
last_time=time.time()
angle = 0



Current_Vel_X=0
Current_Vel_Y=1
Current_Vel_Z=1
Accel_X = 0
Accel_Y = 0
Accel_Z = 0
MagX = 0
MagY = 0
MagZ =0

Max_Glider_Pos=15
Current_Glider_R_Pos=5
Current_Glider_L_Pos=5



Altt_Value=390
Long_Value=100
Latt_Value=200
Vertical_Vel=Current_Vel_Z
Horizontal_Vel=math.sqrt((Current_Vel_X^2)+(Current_Vel_Y^2))
Abs_Vel=math.sqrt((Current_Vel_X^2)+(Current_Vel_Y^2)+(Current_Vel_Z^2))

Compass_angle=0

ETA_Num=Altt_Value/Vertical_Vel

data_recieved=0
data_sent=0
#endregion
#------------------Create Window/Canvas/Images--------------------------------------------------------
#region
window = Tk()
window.title("CanSat Trajectory")
window.geometry("1920x1800")
#------------------Create Canvas'
frame=Frame(window, borderwidth=5, relief="ridge", width=300, height=500)
#
SliderCanvas=Canvas(window, width=300,height=500)
CompassCanvas= Canvas(window, width=1500,height=40)
my_canvas = Canvas(window, width=1500,height=900)
#
my_canvas.grid(row=1,column=0, rowspan=6)
CompassCanvas.grid(row=0,column=0)
frame.grid(row=0,column=1, rowspan=3,sticky="n")
SliderCanvas.grid(row=4,column=1)

#--------Import Images
Google_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/map.png')
PIL_Cansat_Image=Image.open('C:/Users/sebastien/Downloads/Cansat_Arrow.png')
Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
Compass_Image=PhotoImage(file='C:/Users/sebastien/Downloads/Compass.png')
CompassCentre_Image=PhotoImage(file='C:/Users/sebastien/Downloads/CompassCentre.png')
Slider_Background_Image=PhotoImage(file='C:/Users/sebastien/Downloads/Slider_Background.png')
Slider_Slider_Image=PhotoImage(file='C:/Users/sebastien/Downloads/Paraglider bar.png')

#---------Place Inside Canvas
GoogleMap=my_canvas.create_image(750,450,image=Google_Image, anchor='center')
Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")
Compass_Centre=CompassCanvas.create_image(750,40,image=CompassCentre_Image)
Compass=CompassCanvas.create_image(750,20,image=Compass_Image)
Slider_Background=SliderCanvas.create_image(0,0,image=Slider_Background_Image,anchor='nw')
Slider_Slider_1=SliderCanvas.create_image(50,50,image=Slider_Slider_Image)
Slider_Slider_2=SliderCanvas.create_image(200,50,image=Slider_Slider_Image)
#endregion
#-----------------------------------------------------------------------------------
def move_up(event):
    my_canvas.move(GoogleMap,0,+5)
def move_down(event):
    my_canvas.move(GoogleMap,0,-5)
def move_left(event):
    my_canvas.move(GoogleMap,+5,0)
def move_right(event):
    my_canvas.move(GoogleMap,-5,0)

#-----------------------------------------------------------------------------------
def Compass_move_left(event):
    global angle
    angle=angle-0.97
    my_canvas.delete("Cansat_Arrow")
    PIL_Cansat_Image=Image.open('C:/Users/sebastien/Downloads/Cansat_Arrow.png')
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

#def Rotate_Cansat_Arrow():

#----------------------------------------------------------------------------------------------
def Move_Left_Slider_Up(event):
    global Current_Glider_L_Pos
    if Current_Glider_L_Pos<Max_Glider_Pos:
        SliderCanvas.move(Slider_Slider_1,0,-5)
        Current_Glider_L_Pos=Current_Glider_L_Pos+1
def Move_Left_Slider_Down(event):
    SliderCanvas.move(Slider_Slider_1,0,+5)
def Move_Right_Slider_Up(event):
    SliderCanvas.move(Slider_Slider_2,0,-5)
def Move_Right_Slider_Down(event):
    SliderCanvas.move(Slider_Slider_2,0,+5)

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
    


Altt = Label(frame,text="Altt: ",font=("font",30)).grid(row=0,column=1)
AlttNum = Label(frame,text=Altt_Value,font=("font",30)).grid(row=0,column=2)
Long = Label(frame,text="Long: ",font=("font",30)).grid(row=1,column=0)
LongNum = Label(frame,text=Long_Value,font=("font",30)).grid(row=1,column=1)
Latt = Label(frame,text="Latt: ",font=("font",30)).grid(row=1,column=2)
LattNum = Label(frame,text=Latt_Value,font=("font",30)).grid(row=1,column=3)

H_Vel = Label(frame,text="H. Vel: ",font=("font",30)).grid(row=2,column=0)

V_Vel = Label(frame,text="V. Vel: ",font=("font",30)).grid(row=2,column=2)
V_Vel_Num = Label(frame,text=Vertical_Vel,font=("font",30)).grid(row=2,column=3)

Eta = Label(frame,text="ETA: ",font=("font",30)).grid(row=3,column=0)
Eta_Num = Label(frame,text=ETA_Num,font=("font",30)).grid(row=3,column=1)

#Radio_info=Label(frame,text=Radio_Sen,font=("font",30)).grid(row=4,column=0,column_span=4,row_span=4)

#---------Place Inside Grid----------------------------------------------------------------------------------------






#
#my_canvas.itemconfig(Cansat_Arrow,image=Cansat_Image)

#CS = DigitalInOut(board.CE1)
#RESET = DigitalInOut(board.D25)
#spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

window.mainloop()
'''while True:

    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
        print("radio detected")
    except RuntimeError as error:
        print('RFM9x Error: ', error)
    
    packet = rfm9x.receive()
    if packet is None:
        print("Waiting for packet")
    else:
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print(packet_text)
        data_recieved=packet_text.split(", ")
    
    data_sent="%d, %d".format(Current_Glider_R_Pos,Current_Glider_L_Pos)
    rfm9x.send(data_sent)
    
    #PIL_Cansat_Image=Image.open('C:/Users/sebastien/Downloads/Cansat_Arrow.png')
    #global Cansat_Image
    #Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
    #my_canvas.itemconfig(Cansat_Arrow,image=Cansat_Image)
    #Cansat_Arrow.update()
    #window.update()'''
