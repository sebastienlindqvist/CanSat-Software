#-----------------------------------------------------------------------------------
from tkinter import *
from PIL import Image, ImageTk
from PIL import *


#-----------------------------------------------------------------------------------
def move_up(event):
    #CanSat_Arrow.place(x=CanSat_Arrow.winfo_x(),y=CanSat_Arrow.winfo_y()-1)
    my_canvas.move(GoogleMap,0,+5)
def move_down(event):
    #CanSat_Arrow.place(x=CanSat_Arrow.winfo_x(),y=CanSat_Arrow.winfo_y()+1)
    my_canvas.move(GoogleMap,0,-5)
def move_left(event):
    #CanSat_Arrow.place(x=CanSat_Arrow.winfo_x()-1,y=CanSat_Arrow.winfo_y())
    my_canvas.move(GoogleMap,+5,0)
def move_right(event):
    #CanSat_Arrow.place(x=CanSat_Arrow.winfo_x()+1,y=CanSat_Arrow.winfo_y())
    my_canvas.move(GoogleMap,-5,0)
#-----------------------------------------------------------------------------------
def Compass_move_left(event):
    #PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #PIL_Cansat_Image=PIL_Cansat_Image.rotate(10)
    #PIL_Cansat_Image.save('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)



   # PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #Compass_angle=0
    #image = PIL_Cansat_Image
    #tkimage = image.rotate(Compass_angle)
    #tkimage.save('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #tkimage=ImageTk.PhotoImage(tkimage)
    #window.after_idle(draw())
    #yield
    my_canvas.delete("Cansat_Arrow")

    #PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
    #PIL_Cansat_Image=PIL_Cansat_Image.rotate(10)
    #Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)
    #Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")
    

    
    
    CompassCanvas.move(Compass,-5,0)

    if CompassCanvas.coords(Compass)[0] <= -25:
        #print("Hello")
        CompassCanvas.move(Compass,+1855,0)


def Compass_move_right(event):
    #CanSat_Arrow.place(x=CanSat_Arrow.winfo_x()+1,y=CanSat_Arrow.winfo_y())
    CompassCanvas.move(Compass,+5,0)
    if CompassCanvas.coords(Compass)[0] >= 1830:
        CompassCanvas.move(Compass,-1855,0)
#------------------Create Window--------------------------------------------------------
window = Tk()
window.title("CanSat Trajectory")
window.geometry("1920x1800")
#------------------Bind Keys----------------------------------------------------------------
window.bind("<w>",move_up)
window.bind("<s>",move_down)
window.bind("<a>",move_left)
window.bind("<d>",move_right)
window.bind("<e>",Compass_move_left)
window.bind("<q>",Compass_move_right)
#------------------Create Canvas-------------------------------------------------------------------
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

#--------Import Images-------------------------------------------------------------------------------------------
Google_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/map 2021-07-03 220540.png')

PIL_Cansat_Image=Image.open('C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
Cansat_Image=ImageTk.PhotoImage(PIL_Cansat_Image)

Compass_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Compass.png')
CompassCentre_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/CompassCentre.png')
Slider_Background_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Slider Background.png')
#Slider_Slider=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/')
#-----------Creating Labels and Others---------------------------------------------------------------------------------
'''AccelX = 
AccelY = 
AccelZ =
MagX = 
MagY = 
MagZ ='''
Altt_Value=390
Long_Value=100
Latt_Value=200
Vertical_Vel=300
Horizontal_Vel=3
Abs_Vel=56

Compass_angle=0

Altt = Label(frame,text="Altt: ",font=("font",30)).grid(row=0,column=1)
AlttNum = Label(frame,text=Altt_Value,font=("font",30)).grid(row=0,column=2)
Long = Label(frame,text="Long: ",font=("font",30)).grid(row=1,column=0)
LongNum = Label(frame,text=Long_Value,font=("font",30)).grid(row=1,column=1)
Latt = Label(frame,text="Latt: ",font=("font",30)).grid(row=1,column=2)
LattNum = Label(frame,text=Latt_Value,font=("font",30)).grid(row=1,column=3)




#---------Place Inside Grid----------------------------------------------------------------------------------------




#---------Place Inside Canvas---------------------------------------------------------------------------------------
GoogleMap=my_canvas.create_image(0,0,image=Google_Image)
Cansat_Arrow=my_canvas.create_image(750,450,image=Cansat_Image,tag="Cansat_Arrow")
Compass_Centre=CompassCanvas.create_image(750,40,image=CompassCentre_Image)
Compass=CompassCanvas.create_image(750,20,image=Compass_Image)
Slider_Background=SliderCanvas.create_image(0,0,image=Slider_Background_Image,anchor='nw')

#

window.mainloop()