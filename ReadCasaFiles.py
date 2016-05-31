# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description:
Input(s):
Output(s):
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
"""
#------------Load Python Modules--------------------#
from netCDF4 import Dataset
import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#---------------------Define Directories and file list---------------------#

os.chdir('C://Users//slawler//Desktop//10-min')    
grids = glob('*.nc')

hms_basins = 'P:\Temp\sreetharan\Texas_HMS_RAS\shapefiles\SubbasinHRAP'

#------------------------------Define Functions-----------------------#
def plot_garland(lon_min, lat_min,lon_max,lat_max):
    """ Create a plot of Texas. """
    m = Basemap(
        llcrnrlon=-lon_min,
        llcrnrlat=lat_min,
        urcrnrlon=lon_max,
        urcrnrlat=lat_max,
        projection='mill',
        resolution='f')

    m.readshapefile(hms_basins,'SubbasinHRAP',drawbounds=True)
    return m


for grid in grids:
    print grid
    
    f = Dataset(grid,'r')
    
    lons   = f.variables['Longitude'][:]
    lats   = f.variables['Latitude'][:]
    precip = f.variables['rain_10min'][:]
    
    f.close()
    
    m = plot_garland(min(lons), min(lats), max(lons), max(lats))
               
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)            
             
                
    # Plot Data
    cs = m.pcolor(xi,yi,np.squeeze(precip))
    
    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label('mm')
    
    # Add Title
    plt.title('Precipitation 10 min /n %s' %grid)
    
    plt.savefig('%s.png' % grid, dpi = 400) 
    plt.close()        

