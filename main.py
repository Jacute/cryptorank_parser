#!/usr/bin/python3.8
import time
from datetime import datetime
import traceback
import requests
import json


URLS = ['https://api.cryptorank.io/v0/coins/bitcoin/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/ethereum/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/litecoin/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/bitcoin-cash/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/ripple/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/cardano/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/solana/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/polkadot/tickers?includeQuote=false',
        'https://api.cryptorank.io/v0/coins/dogecoin/tickers?includeQuote=false']

abbrs = {'https://api.cryptorank.io/v0/coins/bitcoin/tickers?includeQuote=false': 'BTC/USDT',
        'https://api.cryptorank.io/v0/coins/ethereum/tickers?includeQuote=false': 'ETH/USDT',
        'https://api.cryptorank.io/v0/coins/litecoin/tickers?includeQuote=false': 'LTC/USDT',
        'https://api.cryptorank.io/v0/coins/bitcoin-cash/tickers?includeQuote=false': 'BCH/USDT',
        'https://api.cryptorank.io/v0/coins/ripple/tickers?includeQuote=false': 'XRP/USDT',
        'https://api.cryptorank.io/v0/coins/cardano/tickers?includeQuote=false': 'ADA/USDT',
        'https://api.cryptorank.io/v0/coins/solana/tickers?includeQuote=false': 'SOL/USDT',
        'https://api.cryptorank.io/v0/coins/polkadot/tickers?includeQuote=false': 'DOT/USDT',
        'https://api.cryptorank.io/v0/coins/dogecoin/tickers?includeQuote=false': 'DOGE/USDT'}

while True:
    try:
        dct = {}
        for url in URLS:
            src = requests.get(url).text
            a = json.loads(src)
            for i in a['data']:
                if i['symbol'] == abbrs[url]:
                    wallet = i['symbol']
                    name = i['exchangeName']
                    if name in ['ZB.COM', 'Bgogo', 'Indodax', 'VinDAX', 'CoinEgg', 'CREX24', 'BW.com',
                                'OceanEx', 'Stex', 'BigONE', 'BitMart', 'Lbank', 'Coinsbit',
                                'Probit', 'CoinTiger']:
                        continue
                    course = i['usdLast']
                    if wallet in ['BTC/USDT', 'ETH/USDT']:
                        course = int(course)
                    elif wallet in ['LTC/USDT', 'BCH/USDT', 'SOL/USDT', 'DOT/USDT']:
                        course = round(course, 2)
                    elif wallet in ['XRP/USDT', 'ADA/USDT']:
                        course = round(course, 3)
                    elif wallet in ['DOGE/USDT']:
                        course = round(course, 4)
                    if wallet not in dct:
                        dct[wallet] = {name: course}
                    else:
                        dct[wallet] = {**dct[wallet], name: course}
        dct['time'] = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        with open('result.json', "w") as write_file:
            json.dump(dct, write_file)
    except Exception:
        print(traceback.format_exc())
