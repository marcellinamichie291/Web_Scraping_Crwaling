import jwt
import hashlib
import requests
import uuid
import re
import multiprocessing as mp

import pandas
import time
import asyncio
import websockets
import json
import fetch_ohlcv_csv

from urllib.parse import urlencode, unquote

access_key = "zaSH0y5YKUaYT9oT10T1plSErpMxFeESHpUujdLu"
secret_key = "27Wxi9lNqThs5pUUtmrpZexZ3fMsSNqDFptL2okc"
server_url = "https://api.upbit.com"

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4())
}

jwt_token = jwt.encode(payload, secret_key)
authorization = 'Bearer {}'.format(jwt_token)
headers = {
    "Authorization" : authorization
}

def get_balances_my():
    res = requests.get(server_url + '/v1/accounts', headers=headers)
    re_rule = re.compile('[0-9]')
    res_check = int("".join(re_rule.findall(str(res))))
    if res_check != 200:
        print("로그인 에러! URL, KEY, JWT_TOKEN 등 재확인 요망")
        return -1
    print("로그인 완료, 잔고 조회 중...")
    result = res.json()
    for i in result:
        print(i['currency'], "잔고 : ", i['balance']) 

async def get_balance_all(q):
    url = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(url, ping_interval = 60) as websocket:
        subscribe_fmt = [
            {"ticket":"test"},
            {
                "type": "ticker",
                "codes": ["KRW-BTC"],
                "isOnlyRealtime": True
            },
            {"format":"SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data) # 구독 요청을 서버에 전송
        
        while True: # 반복적으로 데이터 송신(무한루프)
            data = await websocket.recv() #데이터 송신
            data = json.loads(data) #JSON을 딕셔너리로
            print('현재 시간 :{0}, {1} Price = {2}'.format(time.strftime('%H:%M:%S'),data['cd'],data['tp']))
        
def SubProcess1(q):
    asyncio.run(main(q))

async def main(q):
    await get_balance_all(q)

def price_minutes(ticker, unit):
    url = "https://api.upbit.com/v1/candles/minutes/" + unit
    querystring = {"market":ticker, "count":200}
    res = requests.get(url, headers=headers, params = querystring)
    result = json.loads(res.text) #JSON to dict
    for jsons in result:
        print(jsons['candle_date_time_kst'])
        print(jsons['opening_price'])
    
#프로그램 메인부(main process)
if __name__ == '__main__':
    is_program_exit = 0
    print("-----Upbit Trading Promgram-----")
    while is_program_exit == 0:
        print("\nPlease enter a command to continue...\
        \n 1. 잔고조회\
        \n 2. 거래 가능한 자산 조회\
        \n 3. 과거 자산 가격 데이터 저장하기\
        \n 0. 종료")
        user_input = int(input())
        if user_input == 1:
            get_balances_my()
        elif user_input == 2:
            q = mp.Queue()
            sub_p = mp.Process(name="SubProcess1", target=SubProcess1, args=(q,), daemon=True)
            sub_p.start()
        elif user_input == 3:
            market_ticker = input("티커 입력.. ex) KRW-BTC, BTC-IMX : ")
            time_unit = input("분 단위 입력.. ex) 1,3,5,10,15,30,60,240 : ")
            price_minutes(market_ticker, time_unit)
        elif user_input == 0:
            print("프로그램 종료...")
            break
