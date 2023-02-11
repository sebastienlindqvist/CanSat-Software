from tkinter import *


def move_up(event):
    CanSat_Arrow.place(x=CanSat_Arrow.winfo_x(),y=CanSat_Arrow.winfo_y()-1)

def move_down(event):
    CanSat_Arrow.place(x=CanSat_Arrow.winfo_x(),y=CanSat_Arrow.winfo_y()+1)

def move_left(event):
    CanSat_Arrow.place(x=CanSat_Arrow.winfo_x()-1,y=CanSat_Arrow.winfo_y())

def move_right(event):
    CanSat_Arrow.place(x=CanSat_Arrow.winfo_x()+1,y=CanSat_Arrow.winfo_y())



window = Tk()
window.title("CanSat Trajectory")
window.geometry("1920x1800")

window.bind("<w>",move_up)
window.bind("<s>",move_down)
window.bind("<a>",move_left)
window.bind("<d>",move_right)



#--------------------------------------------------------------------------------------------
Google_Image=PhotoImage(file='map 2021-07-03 220540.png')
GoogleMap=Label(window,image=Google_Image)
GoogleMap.place(x=0,y=0)

#------------------------------------------------------------------------------------------
Cansat_Image=PhotoImage(file='C:/Users/sebas/PythonFolder/Cansat/Cansat_Arrow.png')
CanSat_Arrow=Label(window,image=Cansat_Image)
CanSat_Arrow.place(x=0,y=0)


#
window.wm_attributes('-transparentcolor','gray')
window.mainloop()