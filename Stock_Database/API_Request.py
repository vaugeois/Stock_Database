# -*- coding: utf-8 -*-
"""
@author: Antoine Vaugeois
"""
import requests
import time


def get_data(symbol):
    API_KEY="G2GH1YX1LOC6GTFU"
    req="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+symbol+"&outputsize=full&apikey="+'"'+API_KEY+'"'
    try:
    
        request = requests.request('GET',req,)
        json_data = request.json()['Time Series (Daily)']
        if(json_data!=[None]):
            return json_data
        else:
            return None
    except:
        return None

def asset_data(symbol):
    datas=get_data(symbol)
    liste=[]
    append=liste.append
    for key,data in datas.items():
        tmp=(key,data['1. open'],data['4. close'],data['2. high'],data['3. low'],data['5. volume'])
        append(tmp)
    return liste