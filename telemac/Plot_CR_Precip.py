# -*- coding: utf-8 -*-
"""
Created on Mon May 30 19:53:45 2016

@author: slawler
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#import netCDF4


def plot_cameron(lllon, lllat, urlon,urlat,shape):
    """ Create a plot of the Continential US. """
    m = Basemap(
        llcrnrlon=lllon,
        llcrnrlat=lllat,
        urcrnrlon=urlon,
        urcrnrlat=urlat,
        projection='mill',
        resolution='c')
    #m.drawcoastlines()
    #m.drawcountries()
    #m.bluemarble()
    m.readshapefile(shape,'GlobalWatershed',drawbounds=True)
    return m

lllon,lllat  = -78.0, 38.5 
urlon,urlat  = -77.0, 39.5
shape = '/home/slawler/Documents/cameron_shape/GlobalWatershed'

# Colorbar with NSW Precip colors
nws_precip_colors = [
    "#04e9e7",  # 0.01 - 0.10 inches
    "#019ff4",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
    "#fdfdfd"   # 10.00+
]
precip_colormap = matplotlib.colors.ListedColormap(nws_precip_colors)


# latitude and longitudes of HRAP grid
HRAP_XOR = 945
HRAP_YOR = 540


def lat_lon_from_hrap(hrap_x, hrap_y):
    """ Calculate the latitude and longitude for a HRAP grid. """
    raddeg = 57.29577951
    earthrad = 6371.2
    stdlon = 105.
    mesh_len = 4.7625

    tlat = 60. / raddeg
    x = hrap_x - 401.
    y = hrap_y - 1601.
    rr = x * x + y * y
    gi = ((earthrad * (1 + np.sin(tlat))) / mesh_len)
    gi = gi * gi

    ll_y = np.arcsin((gi - rr) / (gi + rr)) * raddeg
    ang = np.arctan2(y, x) * raddeg
    if (ang < 0):
        ang = ang + 360.

    ll_x = 270 + stdlon - ang
    if (ll_x < 0):
        ll_x = ll_x + 360
    if (ll_x > 360):
        ll_x = ll_x - 360
    return ll_x, ll_y


lats = np.empty((9, 10), dtype='float')
lons = np.empty((9, 10), dtype='float')

for i in xrange(9):
    for j in xrange(10):
        hrap_x = j + HRAP_XOR + 0.5
        hrap_y = i + HRAP_YOR + 0.5
        lon, lat = lat_lon_from_hrap(hrap_x, hrap_y)
        lats[i, j] = lat
        lons[i, j] = -lon

# read in the data, convert in inches


# plot the data
m = plot_cameron(lllon, lllat, urlon,urlat,shape)
levels = [0.01, 0.1, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
          6.0, 8.0, 10., 20.0]
norm = matplotlib.colors.BoundaryNorm(levels, 15)
cax = m.pcolormesh(lons, lats, precip_in, latlon=True, norm=norm,
                   cmap=precip_colormap)
m.colorbar(cax)
#plt.savefig('conus_plot.png', dpi=200)
