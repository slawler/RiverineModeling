# -*- coding: utf-8 - Python 3.5.1 *-
"""
Description:
Input(s):
Output(s):
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
"""
#---------------LOAD PYTHON MODULES-----------------------#
import pandas as pd
import os, requests
from datetime import datetime
from collections import OrderedDict
#---------------ENTER VARIABLES---------------------------#
'''
USGS 01613000 POTOMAC RIVER AT HANCOCK, MD
USGS 01638500 POTOMAC RIVER AT POINT OF ROCKS, MD
USGS 01646500 POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA
'''
PATH      = "/home/slawler/Desktop"           #Download Directory 

gages   = ["01613000","01638500","01646500" ] #Gage List
start     = datetime(1900, 4, 3,0)            #Start Date
stop      = datetime(2015, 5, 1,0)            #End Date
parameter = "00060"                           #Parameter 
format    = "rdb"                             #Format  
url       = 'http://waterservices.usgs.gov/nwis/iv'

#----------------------------------------------------------#
#-----------------------RUN SCRIPT-------------------------#
#----------------------------------------------------------#

#---Loop Through Date Range, Ping URL for data, write data to file      
for i, gage in enumerate(gages):
    print("Grabbing Data for USGS Gage: ", gage)
    first    = datetime.date(start).strftime('%Y-%m-%d')
    last     =  datetime.date(stop).strftime('%Y-%m-%d')    
    params = OrderedDict([('format',format),('sites',gage),('startDT',first), 
                ('endDT',last), ('parameterCD',parameter)])  
    
    r = requests.get(url, params = params) 
    data = r.content.decode()
    newfile = os.path.join(PATH,'%s.txt' % gage)
    
    with open(newfile,'w') as f: f.write(data)
    
    df = pd.read_csv(newfile, sep = '\t',comment = '#')
    df.drop(df.index[[0]], inplace = True)
    df.drop(df.columns[[0,1,3,5]], axis=1,inplace = True)  
    df = df.set_index('datetime')    
    df = df.rename(columns = {'01_00060':'flow'}) 
    
     
         
