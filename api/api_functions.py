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

flow = "00060"  
stage = "00065"

    
def Get_USGS(gage, parameter, start, stop):  
               
    dformat    = "json"                                  # Data Format  
    url        = 'http://waterservices.usgs.gov/nwis/iv' # USGS API
    
    # Format Datetime Objects for USGS API
    first    =  datetime.date(start).strftime('%Y-%m-%d')
    last     =  datetime.date(stop).strftime('%Y-%m-%d') 
    

    # Ping the USGS API for data
    params = OrderedDict([('format',dformat),('sites',gage),('startDT',first), 
                ('endDT',last), ('parameterCD',parameter)])  
    
    r = requests.get(url, params = params) 
    print("\nRetrieved Data for USGS Gage: ", gage)
    data = r.content.decode()
    d = json.loads(data)
    mydict = dict(d['value']['timeSeries'][0])
        
    
    if params['parameterCD'] == '00060':
        obser = "StreamFlow"
    else:
        obser = "Stage"
        
    
    # Great, We can pull the station name, and assign to a variable for use later:
    SiteName = mydict['sourceInfo']['siteName']
    print('\n', SiteName)
    
    
    # After reveiwing the JSON Data structure, select only data we need: 
    tseries = d['value']['timeSeries'][0]['values'][0]['value'][:]
    
    # Create a Dataframe, format Datetime data,and assign numeric type to observations
    df = pd.DataFrame.from_dict(tseries)
    df.index = pd.to_datetime(df['dateTime'],format='%Y-%m-%d{}%H:%M:%S'.format('T'))
    
    df['UTC Offset'] = df['dateTime'].apply(lambda x: x.split('-')[3][1])
    df['UTC Offset'] = df['UTC Offset'].apply(lambda x: pd.to_timedelta('{} hours'.format(x)))
    
    df.index = df.index - df['UTC Offset']
    df.value = pd.to_numeric(df.value)
    
    # Get Rid of unwanted data, rename observed data
    df = df.drop('dateTime', 1)
    df.drop('qualifiers',axis = 1, inplace = True)
    df.drop('UTC Offset',axis = 1, inplace = True)
    df = df.rename(columns = {'value':obser})
    return df




def Get_NOAA(gage, start, stop):
    #--NOAA API https://tidesandcurrents.noaa.gov/api/
    datum     = "msl"   #"NAVD"                  #Datum
    units     = "metric"                         #Units
    time_zone = "gmt"                         #Time Zone
    fmt       = "json"                            #Format
    url       = 'http://tidesandcurrents.noaa.gov/api/datagetter'
    product   = 'water_level'                     #Product
    
    noaa_time_step = '6T'
    noaa = pd.DataFrame()
    gages = dict()
    
    t0     = start.strftime('%Y%m%d %H:%M')
    t1     = stop.strftime('%Y%m%d %H:%M')
    api_params = {'begin_date': t0, 'end_date': t1,
                'station': gage,'product':product,'datum':datum,
                'units':units,'time_zone':time_zone,'format':fmt,
                'application':'web_services' }
        
    pred=[];obsv=[];t=[]
    
    try:
        r = requests.get(url, params = api_params)
        jdata =r.json()
    
        for j in jdata['data']:
            t.append(str(j['t']))
            obsv.append(str(j['v']))
            pred.append(str(j['s']))
        colname = str(gage)    
        noaa[colname]= obsv
        noaa[colname] = noaa[colname].astype(float)
        gages[jdata['metadata']['id']]=jdata['metadata']['name']
    except:
        print(g,'No Data')      
         
    idx = pd.date_range(start,periods = len(noaa.index), freq=noaa_time_step)   
    noaa = noaa.set_index(idx)  
    return noaa
    