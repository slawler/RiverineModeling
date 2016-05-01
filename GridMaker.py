# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 10:38:22 2016

@author: sml
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:00:26 2015
Create a grid file for HEC-HMS
@author: slawler
"""
'''
sub1	GridCell	961	545	0.649917
sub2	GridCell	961	545	2.490273
sub3	GridCell	959	543	0.000483
sub4	GridCell	959	543	0.000483
subname GridCell    coord,coord area (sqkm)
'''

infile = 'CameronRun_GridMaker.txt'
outfile= 'CameronRun.mod'
import numpy as np

with open(infile,'r') as f:
    lines = len(f.readlines())

with open(infile,'r') as f:    
    line = f.readline()
    data = line.split()
    firstx = data[0]
            
head = 'Subbasin: '
tail = 'End:'
blank = '1.00000000000000000'
space= '     '     
s = ' '

 
with open(outfile,'w') as out: 
    l1 = 'Parameter Order: Xcoord Ycoord TravelLength Area'+'\n'+'End:'+'\n'+'\n'
    out.write(l1)


with open(infile,'r') as f:
    with open(outfile,'a') as out:
        x = firstx
        out.write(str(head + x+'\n'))
        for i in np.arange(0,lines):
            line = f.readline()
            data = line.split()
            line;data
            y = data[0]
            if x == data[0]:
                out.write(str(space+ str(data[1]) + s+\
                str(data[2])+ s+str(data[3]) +s+blank+ s+\
                str(data[4])+'\n'))
            else:
                out.write(str(tail + '\n'))
                out.write('\n')
                out.write(str((head) + str(data[0])+'\n'))
                x = data[0]
                out.write(str(space+ str(data[1]) + s+\
                str(data[2])+ s+str(data[3]) +s+blank+ s+\
                str(data[4])+'\n'))
