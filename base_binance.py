from datetime import timedelta
import jwt
import hashlib
import requests
import uuid
import re
import multiprocessing as mp

import pandas as pd
import time
import asyncio

import websockets
import json
import ccxt
import sys
import csv
import os
import fetch_ohlcv_csv

api_key = "2s4kWGvEr7aAXfoSxZlyNoVdPwNHHRw09sJaYvnQzYynU9z1k6VS6mpP2iQKTsZr"
secret_key = "9ti5ltsrcb4pTl3kGNJjJqbKG4hGHvrB4o9xq1R7G2L0cDrS7xRnU8iIe40h29mC"

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret_key,
    'enbaleRateLimit': True,
    'options': {
        'defalutType': 'future'
    }
})

def get_balance_my():
    balance = binance.fetch_balance(params={"type":"future"})
    print(balance['USDT'])

def get_price_ticker(ticker):
    balance = binance.fetch_ticker(ticker)
    print(balance['last'])

def get_price_all(ticker,tf):
    price = binance.fetch_ohlcv(symbol=ticker, timeframe=tf, since=None, limit=5)
    df = pd.DataFrame(price, columns=['Date', 'Open','High','Low','Close','Volume'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace = True)
    print(df)


#프로그램 메인부(main process)
if __name__ == '__main__':
    is_program_exit = 0
    print("-----Binance Trading Promgram-----")
    while is_program_exit == 0:
        print("\nPlease enter a command to continue...\
        \n 1. 잔고 조회\
        \n 2. 티커 현재 가격 조회\
        \n 3. 과거 자산 가격 데이터 조회하기\
        \n 4. 과거 가격 데이터 CSV 저장(BTC ONLY)\
        \n 0. 종료")
        user_input = int(input())
        if user_input == 1:
            get_balance_my()
        elif user_input == 2:
            ticker = input("티커 입력...ex)BTC/USDT : ")
            get_price_ticker(ticker)
        elif user_input == 3:
            ticker = input("티커 입력...ex)BTC/USDT : ")
            timeframe = input("구간 입력...ex)'1d,1h,5m... : ")
            get_price_all(ticker,timeframe)
        elif user_input == 4:
            fetch_ohlcv_csv.scrape_candles_to_csv('BTC_USDT_5m.csv', 'binance', 3, "BTC/USDT", '5m', '2022-05-15T00:00:00Z', 1000) # 2017-08-17T00:00:00Z <- First binance time
        elif user_input == 0:
            print("프로그램 종료...")
            break
