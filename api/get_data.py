# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from datetime import datetime


os.chdir(r"C:\Users\sml\Desktop\RiverineModeling\api")
from api_functions import *

#---USER INPUT
         
# Start date (year, month, day)
y0, m0 ,d0 = 2014, 4, 27          
y1, m1 ,d1 = 2014, 5, 2    
  

# Enter Desired  Data
usgs_gages = {"ANAD2": "01651750", "ACOM2": "01651000", "RVDM2":"01649500"} # ANAD2  
noaa_gages = ['8594900']

#--RUN SCRIPT


# Create Datetime Objects
start     = datetime(y0, m0, d0,0)    
stop      = datetime(y1, m1 ,d1,0) 
run_name  = start.strftime('%b%Y')

# Change to save directroy (create if doesn't exist)
try:
    os.chdir(r"C:\Users\sml\Desktop\FEMA_2009_AnacostiaRiver_HEC_RAS\hindcasts\{}".format(run_name))
except:
    os.mkdir(r"C:\Users\sml\Desktop\FEMA_2009_AnacostiaRiver_HEC_RAS\hindcasts\{}".format(run_name))
    os.chdir(r"C:\Users\sml\Desktop\FEMA_2009_AnacostiaRiver_HEC_RAS\hindcasts\{}".format(run_name))
    
    
#---Get USGS Data
for g in usgs_gages:
    try:
        parameter = flow
        df = Get_USGS(usgs_gages[g],parameter, start, stop)  
        df.to_csv('{}_{}.txt'.format(g, parameter))
    except:
        parameter = stage
        df = Get_USGS(usgs_gages[g],parameter, start, stop)  
        df.to_csv('{}_{}.txt'.format(g, parameter))
    try:
        parameter = stage
        df = Get_USGS(usgs_gages[g],parameter, start, stop)  
        df.to_csv('{}_{}.txt'.format(g, parameter))
    except:
        parameter = flow
        df = Get_USGS(usgs_gages[g],parameter, start, stop)  
        df.to_csv('{}_{}.txt'.format(g, parameter)) 

   
        
#---Get NOAA Data        

for g in noaa_gages: 
    df = Get_NOAA(g, start, stop) 
    df.to_csv('{}.txt'.format(g))              