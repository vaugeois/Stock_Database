# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:21:12 2017
@author: vaugeois
"""

import pandas as pd
import numpy as np
ewma = pd.stats.moments.ewma

#Exponential Moving Average
def mae(data,interval):
    average=ewma(data['close'],com=interval,adjust=False)
    return average.fillna(method='bfill')


#Bollinger Bands
def bollinger(data,interval):
    ma=data['close'].rolling(window=interval).mean()        
    sigma=pd.rolling_std(data['close'], interval, min_periods=interval)
    data['MA']=ma.fillna(method='bfill')
    data['MAsup']=(ma+2*sigma).fillna(method='bfill')
    data['MAinf']=(ma-2*sigma).fillna(method='bfill')
    return data