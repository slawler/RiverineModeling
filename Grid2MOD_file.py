# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:00:26 2015
Create a grid file for HEC-HMS, requires some manual editing of .mod file
@author: slawler

"""

import pandas as pd

infile = 'table.txt'
outfile= 'HecModel.mod'
df = pd.read_csv(infile, sep = '\t')

sub_list = df.Name.sort_values()
subs = sub_list.unique()

header = 'Parameter Order: Xcoord Ycoord TravelLength Area'
trvlng = '1.00000000000000000'
space = ' '
init = '     GridCell: '
end = 'End: \n'
subbasin = 'Subbasin: '

with open('grid.txt','w') as f:
    for i, s in enumerate(subs):
        if i == 0:
            f.write(header + '\n')
            f.write(end)
        idx = df.ix[df['Name'] == s].index.tolist()
        f.write('\n'+subbasin+ s + '\n')
        for j in idx:
            basin = df['Name'].iloc[j]
            x = df['X'].iloc[j]
            y = df['Y'].iloc[j]
            a = df['AreaSqKm'].iloc[j]
            line = init + str(x) +space+ str(y) +space+ trvlng +space+ str(a)
            f.write(line + '\n')
        f.write(end)



