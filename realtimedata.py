# 8PXI9VFLMKI7VXS5 api key

import requests


def market_status():
    url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=8PXI9VFLMKI7VXS5'
    r = requests.get(url)
    market_statusdata = r.json()
    return market_statusdata


def earnings():
    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=MSFT&apikey=8PXI9VFLMKI7VXS5'
    r = requests.get(url)
    earningsdata = r.json()
    return earningsdata

def newstech():
    url = ""
    r = requests.get(url)
    newstechdata = r.json()
    return newstechdata


print(earnings())
