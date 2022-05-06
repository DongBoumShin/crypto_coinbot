import os
import signal
import sys
import time

import pandas
from apscheduler.schedulers.background import BackgroundScheduler
import psutil
import pynput.keyboard as keyboard
import binance

import Algorithm
import Controller


# 필수적인 자료형:
#    데이터프레임: index datetime open high low close volume


def exitprocess():
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        print(child.pid)
        os.kill(child.pid, signal.SIGTERM)
        time.sleep(0.5)
    sys.exit()


class ActualBot:
    def __init__(self):
        user_key = '.'
        secret_key = '.'
        self.binance_client = binance.Client(user_key, secret_key)
        self.hasdict = {}
        self.precisions = {}
        self.soldlist = {}
        self.tiers = [['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'LTCUSDT', 'ETCUSDT'],
                      ['XRPUSDT', 'EOSUSDT', 'TRXUSDT', 'LINKUSDT', 'XLMUSDT'],
                      ['ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'BNBUSDT', 'XTZUSDT'],
                      ['ZECUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT'],
                      ['VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT'],
                      ['ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT'],
                      ['OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT'],
                      ['BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT'],
                      ['DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT'],
                      ['TRBUSDT', 'YFIIUSDT', 'RUNEUSDT', 'SRMUSDT', 'BZRXUSDT'],
                      ['SOLUSDT', 'ICXUSDT', 'AVAXUSDT', 'AXSUSDT', 'LUNAUSDT'],
                      ['FTMUSDT', 'EGLDUSDT', 'FILUSDT', 'DYDXUSDT', 'NEARUSDT']]
        tickers = []
        for tier in self.tiers:
            tickers += tier
        print(tickers)
        self.Algorithm = Algorithm.ExampleAlg(tickers)
        temp = self.binance_client.futures_exchange_info()
        for ticker in tickers:
            self.binance_client.futures_change_leverage(symbol=ticker, leverage=1)
        for info in temp['symbols']:
            if info['symbol'] in tickers:
                self.precisions[info['symbol']] = info['quantityPrecision']
        print(self.precisions)

    def autotrade(self):
        try:
            data15 = None
            data60 = None
            time.sleep(0.1)
            for tier in self.tiers:
                for ticker in tier:
                    if len(self.hasdict.keys()) < 5:
                        soldflag = False
                        if ticker in self.soldlist:
                            soldflag = self.soldlist.pop(ticker, None)
                        if ticker in self.hasdict.values():
                            continue
                        data05 = self.binance_client.futures_klines(symbol=ticker, interval='5m', limit=90)
                        data05 = pandas.DataFrame(data05,
                                                  columns=["date", "open", "high", "low", "close", "volume", 6, 7, 8, 9,
                                                           10, 11])
                        data05.drop([6, 7, 8, 9, 10, 11], axis=1, inplace=True)
                        data05.iat[-2, 4] = data05.iat[-1, 4]
                        data05.drop(89, inplace=True)
                        data05 = data05.apply(pandas.to_numeric)

                        data60 = self.binance_client.futures_klines(symbol=ticker, interval='1h', limit=90)
                        data60 = pandas.DataFrame(data60,
                                                  columns=["date", "open", "high", "low", "close", "volume", 6, 7, 8, 9,
                                                           10, 11])
                        data60.drop([6, 7, 8, 9, 10, 11], axis=1, inplace=True)
                        #data60.drop(89, inplace=True)
                        data60 = data60.apply(pandas.to_numeric)
                        flag, req_info = self.Algorithm.buysell(data05, data15, data60, ticker, soldflag)
                        if flag > 0:
                            position = Controller.Controller(flag, req_info, ticker,
                                                             self.precisions[ticker], self.binance_client)
                            position.get()
                            self.hasdict[position.pid] = ticker
                            print(self.hasdict[position.pid])
                #print(datetime.datetime.now())
                time.sleep(0.5)
            # tier2~5
            print("looped")
        except TimeoutError as te:
            print(te)
            raise TimeoutError

    def main(self):
        full_job = BackgroundScheduler(timezone="Asia/Seoul")
        full_job.add_job(self.autotrade, trigger='cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
        try:
            full_job.start()
			
			def on_press(key):
                if key == keyboard.Key.f11:
                    return False
                if key == keyboard.Key.f10:
                    self.Algorithm.update()

            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            print("started")
            while True:
                for pid in list(self.hasdict.keys()):
                    if not psutil.pid_exists(pid):
                        yeet = self.hasdict.pop(pid)
                        self.soldlist[yeet] = True
                        print(yeet + "sold")
                        time.sleep(1)
                if listener.running is False:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            full_job.shutdown()
            print('quit')
        except TimeoutError as te:
            full_job.shutdown()
            print(te)
        except Exception as e:
            full_job.shutdown()
            print(e)
        exitprocess()


if __name__ == '__main__':
    welp = ActualBot()
    welp.main()
