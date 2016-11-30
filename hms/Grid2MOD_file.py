# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:00:26 2015
Create a grid file for HEC-HMS
@author: slawler

Example File:

Parameter Order: Xcoord Ycoord TravelLength Area
End:

Subbasin: 2C1
     GridCell: 599 256 0.15554718877992446 0.635893
     GridCell: 600 256 0.15554718877992446 4.136621
End:

Subbasin: 2C2
     GridCell: 599 256 0.15554718877992446 0.497083
     GridCell: 598 257 0.15554718877992446 0.127391
     GridCell: 599 257 0.15554718877992446 0.000088
End:

"""


#---Required python modules
import pandas as pd
import os


#---Assign Directory & Path Names

wdir = r"C:\Users\slawler\Documents\LAMP\TEMP" # File Directory
hrap_to_hms_table = 'HRAP_for_HMS.txt'         # Table from ArcGIS
hms_model = 'HecModel'                         # Name of HMS model
Subbasin = 'Name'                              # Column name of the Subbasins 
hrap_x   = 'X_int'                             # Column name of the HRAP X GridCell 
hrap_y   = 'Y_int'                             # Column name of the HRAP Y GridCell
area     = 'Area_sqkm'                         # Column name of the Area in Square Kilometers


# Run Script
f = os.path.join(wdir,hrap_to_hms_table ) # Create a full path to the file
df = pd.read_csv(f, sep = ',')            # Read in data         
subs = df[Subbasin].unique() # Unique Subbasins dissolved during intersect w/HRAP grid

#---HMS Formatted data 
header = 'Parameter Order: Xcoord Ycoord TravelLength Area'
trvlng = '1.00000000000000000'
space = ' '
init = '     GridCell: '
end = 'End: \n'
subbasin = 'Subbasin: '

#  Write .mod file
modfile = os.path.join(wdir, hms_model + '.mod')

with open(modfile,'w') as f:
    for i, s in enumerate(subs):
        if i == 0:
            f.write(header + '\n')
            f.write(end)
        idx = df.ix[df[Subbasin] == s].index.tolist()
        f.write('\n'+subbasin+ s + '\n')
        for j in idx:
            basin = df[Subbasin].iloc[j]
            x = df[hrap_x].iloc[j]
            y = df[hrap_y ].iloc[j]
            a = df[area].iloc[j]
            line = init + str(x) +space+ str(y) +space+ trvlng +space+ str(a)
            f.write(line + '\n')
        f.write(end)

