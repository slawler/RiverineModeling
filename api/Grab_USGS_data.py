# -*- coding: utf-8 - Python 3.5.1 *-
"""
Description: Grab Time Series data From USGS Web Service
Input(s)   : USGS Gages, Parameters
Output(s)  : .rdb time series files
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
"""
# Import libraries
import pandas as pd
import requests
import json
from datetime import datetime
from collections import OrderedDict

# In[ ]:

# Enter Desired Data
gage       = "02053500"                              # USGS Gage    

y0, m0 ,d0 = 2016, 10, 6                             # Start date (year, month, day)
y1, m1 ,d1 = 2016, 10, 13                             # End date


#parameter  = ["00060","00065"]                       # Try Flow first    
parameter  = ["00065","00060"]                       # Try Stage First                    
dformat    = "json"                                  # Data Format  
url        = 'http://waterservices.usgs.gov/nwis/iv' # USGS API



# Create Datetime Objects
start     = datetime(y0, m0, d0,0)    
stop      = datetime(y1, m1 ,d1,0)         

# Format Datetime Objects for USGS API
first    =  datetime.date(start).strftime('%Y-%m-%d')
last     =  datetime.date(stop).strftime('%Y-%m-%d') 


# In[ ]:

# Ping the USGS API for data
try:
    params = OrderedDict([('format',dformat),('sites',gage),('startDT',first), 
                ('endDT',last), ('parameterCD',parameter[0])])  
    
    r = requests.get(url, params = params) 
    print("\nRetrieved Data for USGS Gage: ", gage)
    data = r.content.decode()
    d = json.loads(data)
    mydict = dict(d['value']['timeSeries'][0])
    
except:
    params = OrderedDict([('format',dformat),('sites',gage),('startDT',first), 
                ('endDT',last), ('parameterCD',parameter[1])])  
    
    r = requests.get(url, params = params) 
    print("\nRetrieved Data for USGS Gage: ", gage)
    data = r.content.decode()
    d = json.loads(data)
    mydict = dict(d['value']['timeSeries'][0])

if params['parameterCD'] == '00060':
    obser = "StreamFlow"
else:
    obser = "Stage"
    
    
# In[ ]:

# Great, We can pull the station name, and assign to a variable for use later:
SiteName = mydict['sourceInfo']['siteName']
print('\n', SiteName)


# In[ ]:

# After reveiwing the JSON Data structure, select only data we need: 
tseries = d['value']['timeSeries'][0]['values'][0]['value'][:]


# In[ ]:

# Create a Dataframe, format Datetime data,and assign numeric type to observations
df = pd.DataFrame.from_dict(tseries)
df.index = pd.to_datetime(df['dateTime'],format='%Y-%m-%d{}%H:%M:%S'.format('T'))

df['UTC Offset'] = df['dateTime'].apply(lambda x: x.split('-')[3][1])
df['UTC Offset'] = df['UTC Offset'].apply(lambda x: pd.to_timedelta('{} hours'.format(x)))

df.index = df.index - df['UTC Offset']
df.value = pd.to_numeric(df.value)

# In[ ]:

# Get Rid of unwanted data, rename observed data
df = df.drop('dateTime', 1)
df.drop('qualifiers',axis = 1, inplace = True)
df.drop('UTC Offset',axis = 1, inplace = True)
df = df.rename(columns = {'value':obser})

print("\nTop Rows: \n", df.head())
print("\nBottom Rows: \n", df.tail())

# In[ ]:

# Plot the Results, and use the SiteName as a title!
df.plot(grid = True, title = SiteName)


