import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import sys
import traceback
import json


urls = ['https://cryptorank.io/price/bitcoin/arbitrage',
        'https://cryptorank.io/price/ethereum/arbitrage',
        'https://cryptorank.io/price/litecoin/arbitrage',
        'https://cryptorank.io/price/bitcoin-cash/arbitrage',
        'https://cryptorank.io/price/ripple/arbitrage',
        'https://cryptorank.io/price/cardano/arbitrage',
        'https://cryptorank.io/price/solana/arbitrage',
        'https://cryptorank.io/price/polkadot/arbitrage',
        'https://cryptorank.io/price/dogecoin/arbitrage']


def parse(url, dct):
    try:
        driver.get(url)
        time.sleep(0.5)
        btn = driver.find_elements(By.CLASS_NAME, 'kjJvqN')[1]
        driver.execute_script("window.scrollTo(0, 222);")
        btn.click()
        abbr = driver.find_element(By.CLASS_NAME, 'coin-info__symbol').text[1:-1]
        lst = driver.find_elements(By.XPATH, f"//th[text()='{abbr}/USDT']")
        for i in lst:
            name, course, wallet = i.text.split('\n')
            if name == 'CoinBase ...':
                name = 'CoinBase Pro'
            elif name == 'MEXC Glob...':
                name = 'MEXC Global'
            elif name == 'Huobi Glo...':
                name = 'Huobi Global'
            elif name == 'Pancake S...':
                name = 'Pancake Swap'
            if wallet not in dct:
                dct[wallet] = {name: course}
            else:
                dct[wallet] = {**dct[wallet], name: course}
        return dct
    except Exception as e:
        print(e)
        driver.refresh()
        time.sleep(0.5)
        parse(url, dct)


def main():
    while True:
        dct = {}
        for url in urls:
            dct = parse(url, dct)
        dct['time'] = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        with open("result.json", "w") as write_file:
            json.dump(dct, write_file)
        print('Парсинг успешен! Результаты записаны в result.json')


def get_driver():
    try:
        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

        # for ChromeDriver version 79.0.3945.16 or over
        options.add_argument("--disable-blink-features=AutomationControlled")

        # headless mode
        # options.add_argument("--headless")
        # options.headless = True

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(5)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as e:
        print('Неудачная настройка браузера!')
        print(traceback.format_exc())
        print(input('Нажмите ENTER, чтобы закрыть эту программу'))
        sys.exit()


if __name__ == '__main__':
    driver = get_driver()
    actions = ActionChains(driver)
    try:
        main()
    except Exception:
        print('Ошибка!\n', traceback.format_exc(), f'\nСсылка: {driver.current_url}')
    finally:
        driver.close()
        driver.quit()
        print(input('Нажмите ENTER, чтобы закрыть эту программу'))