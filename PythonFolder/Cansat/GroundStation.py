
#-----------------------Import Libraries----------------------------------------------------------------------

#--
from bokeh.core.property.primitive import Null
from bokeh.io.output import reset_output
import pandas as pd
import os 
#---
from bokeh.models.sources import ColumnDataSource
from bokeh.io import show
from bokeh.plotting import gmap,figure,output_file, show, save
from bokeh.models import GMapOptions, Label, Label, Arrow
#from bokeh.models.tools import HoverTool
from bokeh.embed import components
from bokeh.models.arrow_heads import *
#-------------------------------------------------------------------------------------------------------------
API_KEY = 'AIzaSyBkUWPudWjFc2dGuweZYSDyi6vR8RYxB90'
#-------------------------------------------------------------------------------------------------------------
bokeh_width, bokeh_height = 1600,900

#---------------------------Longitude & Lattitude -----------------------------------------------------------
lat, lon = 55.44622373734394, -5.694747515447235 #machrihanish community airbase
#--------------------------------------------------------------------------------------------------------------


#----------------------Initial/Update CanSat position on Webpage-------------------------------------------------
x=[-5.694747515447235]
y= [55.44622373734394]
s = [10]
source= ColumnDataSource(data=dict(x=x, y=y, size=s))
#---------------------Making of google map webpage----------------------------------------------------------------#
def plot(lat, lng, zoom=17, map_type='hybrid'):
    gmap_options = GMapOptions(lat=lat, lng=lng, map_type=map_type, zoom=zoom)
    p = gmap(API_KEY, gmap_options, title='CanSat geolocation', width=bokeh_width, height=bokeh_height) 
    #tools="pan,box_select,zoom_in,zoom_out,save,reset")
    return p
#-----------------------------------------------------------------------------------------------------------------#
p = plot(lat, lon)



#---------Render Glyphs--------------------#
#---------------------Making of Cansat red dot-------------------------------------------------------------#
center = p.circle('x', 'y', size='size',source=source, alpha=1, color='red')
arrow = p.add_layout(Arrow(end=NormalHead(fill_color="orange"),x_start=x[0],y_start=y[0],x_end=(x[0]+2),y_end=(y[0]+0.5)))
#----------------------------------------------------------------------------------------------------------#
#def update_size():]



# Add tooltips
#hover = HoverTool()
#hover.tooltips="""
    #<div>
        #<h3>@Cansat</h3>
        #<div><strong>long: </strong>@x</div>
        #<div><strong>Latt: </
        # strong>@y</div>
#</div>
#"""



#p.add_tools(hover)
#-----Opening and showing the Webpage--------------------------------------------------------------------------------
show(p) #this is static and doesn't change. Opens a new tab
#save(p) #this is saved as a html file. Doesn't open a tab. requires html, live server to be installed.
#center = p.circle('x', 'y', size='size',source=source, alpha=1, color='red')

#--------------------------------------------------------------------------------------------------------------------





#lat1=0
#while True:
    #print(x[0])
    #x[0]=x[0]-0.01
    
    #p.update()
    #source= ColumnDataSource(data=dict(x=x, y=y, size=s))
    #center.update()
    #p = plot(lat, lon)
    #p = plot(lat, lon, lon1, lat1)
    #lat1=lat1+0.01

