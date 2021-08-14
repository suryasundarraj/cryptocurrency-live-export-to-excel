#!/usr/bin/python3
# coding: utf-8

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import os
import pandas as pd 
import csv

pp = pprint.PrettyPrinter(indent=4)


# This creates a long string of all the top 100 crypto currency symbols.
symbolstr=','.join(('BTC,ETH,BNB,XRP,USDT,ADA,DOT,UNI,LTC,LINK,XLM,BCH', 
        'THETA,FIL,USDC,TRX,DOGE,WBTC,VET,SOL,KLAY,EOS,XMR,LUNA', 
        'MIOTA,BTT,CRO,BUSD,FTT,AAVE,BSV,XTZ,ATOM,NEO,AVAX,ALGO', 
        'CAKE,HT,EGLD,XEM,KSM,BTCB,DAI,HOT,CHZ,DASH,HBAR,RUNE,MKR,ZEC',
        'ENJ,DCR,MKR,ETC,GRT,COMP,STX,NEAR,SNX,ZIL,BAT,LEO,SUSHI', 
        'MATIC,BTG,NEXO,TFUEL,ZRX,UST,CEL,MANA,YFI,UMA,WAVES,RVN',
        'ONT,ICX,QTUM,ONE,KCS,OMG,FLOW,OKB,BNT,HNT,SC,DGB,RSR,DENT',
        'ANKR,REV,NPXS,VGX,FTM,CHSB,REN,IOST,BTMX,CELO,PAX,CFX'))
    
# Makes symbolstr into a list for later for loop
symbol_list=symbolstr.split(',')

url= f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': "7ad4c03c-9587-43c7-a266-5378b5015c5e",
}
parameters = {
  'symbol':symbolstr
  }
session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    data = json.loads(response.text)

#pp.pprint(data)
line_list=[]
for symbol in symbol_list:
    thename=data['data'][symbol]['name']
    cid=data['data'][symbol]['id']
    cirsup = data['data'][symbol]['circulating_supply']
    date = data['data'][symbol]['last_updated']
    market_cap = data['data'][symbol]['quote']['USD']['market_cap']
    percent_change_24h = data['data'][symbol]['quote']['USD']['percent_change_24h']
    percent_change_7d = data['data'][symbol]['quote']['USD']['percent_change_7d']
    volume_24h = data['data'][symbol]['quote']['USD']['volume_24h']
    line=[cid, thename, symbol, cirsup, date, market_cap, volume_24h, percent_change_24h, percent_change_7d]
    line_list.append(line)
df = pd.DataFrame(line_list, columns =['ID', 'Name', 'Symbol', 'Circulating Supply', 'Last Update', 'Market Cap','Volume(24h)', '%_24h', '%_7d'])

url= f'https://api.wazirx.com/api/v2/market-status'
headers = {
    'Accepts': 'application/json'
}

try:
    response = session.get(url, params=parameters)
    wdata = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    wdata = json.loads(response.text)

#pp.pprint(wdata)
df_json = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in wdata.items() ]))

with pd.ExcelWriter('coinmap.xlsx') as writer:  
    df.to_excel(writer,sheet_name='coinmarketcap')
    df_json.to_excel(writer,sheet_name='wazirx')