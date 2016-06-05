# -*- coding: utf-8 -*-
"""
Created on Sat Jun 04 08:02:12 2016

Description: Under Construction! Convert netcdf to dss grids, SHG format
Input: netcdf
Output: plots, txt files, dss (eventually)

@author: sml
"""
#------------Import Python Modules-----------#
#import sys
from netCDF4 import Dataset
from pyproj import Proj
import gdal
import sys
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

#------------Begin Script--------------------#
    
def DecDeg2SHG(x,y,cellsize):
    #Asssign Projection Converstion Function
    p = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +x_0=0 +y_0=0                            +ellps=GRS80 +datum=NAD83 +units=m +no_defs ')
    #Convert x,y pair to aea    
    x1,y1 = p(x,y)   
    #Convert aea coordinates to SHG grid
    grid_x, grid_y  = int(np.floor(x1)/cellsize),int(np.floor(y1)/cellsize)    
    return grid_x, grid_y
        
#---Read in netcdf file, take a look at it
nc_file = '29May2015_030800_10min.nc'

f = Dataset(nc_file,'r')
lons   = f.variables['Longitude'][:]
lats   = f.variables['Latitude'][:]
precip = f.variables['rain_10min'][:]
f.close()

#Initialize column/row values
rows =[] ; cols=[]

#---Get Row Assignments
for x in lons:
    xy = ToAlbers(x,lats[0])
    colname = DecDeg2SHG(x,y,250)
    cols.append(colname[0])
cols = np.array(cols)

#---Get Column Assignments    
for y in lats:
    xy = ToAlbers(lons[0],y)
    rowname = DecDeg2SHG(x,y,250)
    rows.append(rowname[1])
rows = np.array(rows)

#---Read Gridded Precip into Dataframe with row/col names
df = pd.DataFrame(precip, columns = cols, index =rows)
df.head()
df.to_csv('%s.txt' % nc_file[:-3], sep = '\t')


#---Plot dataframe
plt.pcolormesh(df)
plt.yticks(np.arange(0.5, len(df.index), 100), df.index)
plt.xticks(np.arange(0.5, len(df.columns), 100), df.columns)
plt.title('Duck Creek, HEC-HMS SHG Grid')
plt.colorbar()
plt.show()
       
'''
#---Make a dictionary for all grid cells
SHG_Grid = {}
for i in lats:
    print i
    for j in lons: 
        print i, j
        x1,y1 = ToAlbers(j,i)        
        grid_x, grid_y  = int(np.floor(x1)/250),int(np.floor(y1)/250)
        SHG_Grid[i,j]=x1,y1         
        print grid_x, grid_y

#==========================================================================#
#---Make a Fishnet grid 
xmin,xmax            = -80000,-25000 #min(lons),max(lons)
ymin,ymax            = -860000, -810000 #min(lats),max(lats)
gridHeight,gridWidth = 500,500

#main('shgGrid_5',xmin,xmax,ymin,ymax,gridHeight,gridWidth)
'''
