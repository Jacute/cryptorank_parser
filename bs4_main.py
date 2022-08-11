#!/usr/bin/python3.8
import json
from datetime import datetime

from bs4 import BeautifulSoup
import subprocess
import traceback
import requests
import time
from random import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import re


MATCH_ALL = r'.*'
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

user_agent = user_agent_rotator.get_random_user_agent()


urls = ['https://cryptorank.io/price/bitcoin/arbitrage',
        'https://cryptorank.io/price/ethereum/arbitrage',
        'https://cryptorank.io/price/litecoin/arbitrage',
        'https://cryptorank.io/price/bitcoin-cash/arbitrage',
        'https://cryptorank.io/price/ripple/arbitrage',
        'https://cryptorank.io/price/cardano/arbitrage',
        'https://cryptorank.io/price/solana/arbitrage',
        'https://cryptorank.io/price/polkadot/arbitrage',
        'https://cryptorank.io/price/dogecoin/arbitrage']

abbrs = {'https://cryptorank.io/price/bitcoin/arbitrage': 'BTC',
        'https://cryptorank.io/price/ethereum/arbitrage': 'ETH',
        'https://cryptorank.io/price/litecoin/arbitrage': 'LTC',
        'https://cryptorank.io/price/bitcoin-cash/arbitrage': 'BCH',
        'https://cryptorank.io/price/ripple/arbitrage': 'XRP',
        'https://cryptorank.io/price/cardano/arbitrage': 'ADA',
        'https://cryptorank.io/price/solana/arbitrage': 'SOL',
        'https://cryptorank.io/price/polkadot/arbitrage': 'DOT',
        'https://cryptorank.io/price/dogecoin/arbitrage': 'DOGE'}


def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, return None.
    If more than one match is found, raise ValueError.
    """
    elements = soup.find_all(tag, **kwargs)
    matches = []
    for element in elements:
        if element.find(text=like(text)):
            matches.append(element.text)
    return matches


def main():
    dct = {}
    for url in urls:
        try:
            user_agent = user_agent_rotator.get_random_user_agent()
            header = {
                'user_agent': user_agent
            }
            src = requests.get(url, headers=header).text
            soup = BeautifulSoup(src, 'lxml')
            wallet = abbrs[url] + '/USDT'
            lst = find_by_text(soup, wallet, 'th')
            if lst != []:
                for i in lst:
                    name = i.split('$ ')[0]
                    course = re.findall(r'\d+\.\d+', i.replace(',', '.'))[0]
                    if name == 'Huobi Glo...':
                        name = 'Huobi Global'
                    elif name == 'Pancake S...':
                        name = 'Pancake Swap'
                    elif name == 'CoinBase ...':
                        name = 'CoinBase Pro'
                    elif name == 'Binance U' or name == 'Binance US':
                        continue
                    if wallet not in dct:
                        dct[wallet] = {name: course}
                    else:
                        dct[wallet] = {**dct[wallet], name: course}
            else:
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(src)
                dct[wallet] = {}
            time.sleep(random())
        except Exception:
            print('Ошибка! Перезапускаем парсер\n' + traceback.format_exc())
            time.sleep(5 + random())
            return 0
    dct['time'] = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    with open('result.json', "w") as write_file:
        json.dump(dct, write_file)
    print('Парсинг успешен! Результаты записаны в result.json')
    time.sleep(1 + random())


if __name__ == '__main__':
    try:
        while True:
            main()
    except Exception:
        print('Ошибка!\n', traceback.format_exc())
