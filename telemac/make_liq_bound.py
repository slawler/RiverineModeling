# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd

dfq = '/Users/slawler/vmshare/harvey_buff_river/q_08074000.tsv'
dfs = '/Users/slawler/vmshare/harvey_buff_river/s_08074710.tsv'


# Start with Flow
df = pd.read_csv(dfq, skiprows=26, sep='\t')
df.drop(labels=0, axis=0, inplace=True)

# Format Units #cfs to cms = 0.028
df['Q'] = pd.to_numeric(df['140432_00060'])*0.028

# NOTICED SOME ISSUES WITHT THE DEV DATASET, DROPPING 0'S FROM FLOW FILE
no_value_idx = qt.query('Q == 0').index
df['Q'].iloc[no_value_idx] = np.nan

qt = df[['datetime','Q']].interpolate().copy()

# Next do stage
df = pd.read_csv(dfs, skiprows=26, sep='\t')
df.drop(labels=0, axis=0, inplace=True)

# Format Units #f to m = 0..3048
df['S'] = pd.to_numeric(df['140454_63158'])*0.3048

st = df[['datetime', 'S']]

# Merge Results
df = pd.merge(qt, st, on = 'datetime', how = 'inner')


# Format Datetime
df['dtm'] = pd.to_datetime(df['datetime'])
t0 = df['dtm'].iloc[0]
df['diff'] = df['dtm'] - t0
df['t'] = df['diff'].dt.seconds



df = df[['t', 'Q', 'S']]

station_elevation = -0.2

df['S'] = df['S'] + station_elevation

df.to_csv('bufbay.liq',index=False, sep=' ')