import datetime
import multiprocessing as mp
import asyncio
import csv
import binance


class Controller(mp.Process):
    def __init__(self, longshort, req_info, ticker, precision, binance_client):
        self.longshort = longshort
        self.target = req_info[0]
        self.stoploss = req_info[1]
        self.avprice = req_info[2]
        self.atr_var = req_info[3]
        self.ticker = ticker
        self.binance_client = binance_client
		with open("price_data.json", 'r') as file:
        	price_data=json.load(file)
        self.amount = price_data['amount'] # dollars
        self.leverage = price_data['leverage']
        self.coin = round(self.amount/self.avprice, precision)
        self.alive = False
        self.stdate = None
        super().__init__()

    async def __connect_socket_long(self):
        # everything_done_here
        # connect
        # get price
        # update target/stoploss
        # forever
        client = await binance.AsyncClient.create()
        bm = binance.BinanceSocketManager(client)
        ts = bm.symbol_mark_price_socket(self.ticker)
        async with ts as tscm:
            while self.alive:
                recv_data = await tscm.recv()
                price = float(recv_data['data']['p'])
                if price > self.target:
                    print(self.ticker+"won_l")
                    self.target += 1.9*self.atr_var
                    self.stoploss = price - 0.5*self.atr_var
                if price < self.stoploss: #or price < self.avprice*0.99:
                    print(self.ticker+"stoploss_l")
                    self.endphase(price)
                    await client.close_connection()
                    self.terminate()

    async def __connect_socket_short(self):
        # everything_done_here
        # connect
        # get price
        # update target/stoploss
        # forever
        client = await binance.AsyncClient.create()
        bm = binance.BinanceSocketManager(client)
        ts = bm.symbol_mark_price_socket(self.ticker)
        async with ts as tscm:
            while self.alive:
                recv_data = await tscm.recv()
                price = float(recv_data['data']['p'])
                if price < self.target:
                    self.target -= 1.9 * self.atr_var
                    self.stoploss = price + 0.5*self.atr_var
                    print(self.ticker+"won_sh")
                if price > self.stoploss:# or price > self.avprice*1.01:
                    print(self.ticker+"stoploss_sh")
                    self.endphase(price)
                    await client.close_connection()
                    self.terminate()

    def run(self):
        # 사고팔기
        self.__aloop = asyncio.get_event_loop()
        self.stdate = datetime.datetime.now()
        if self.longshort == 1:
            #open long
            self.binance_client.futures_create_order(symbol=self.ticker, side='BUY', type='MARKET', quantity=self.coin)
            print("longed")
            self.__aloop.run_until_complete(self.__connect_socket_long())
        elif self.longshort == 2:
            #open short
            self.binance_client.futures_create_order(symbol=self.ticker, side='SELL', type='MARKET', quantity=self.coin)
            print("shorted")
            self.__aloop.run_until_complete(self.__connect_socket_short())

    def get(self):
        # open position
        if not self.alive:
            self.alive = True
        self.start()

    def endphase(self, price):
        self.alive = False
        # 여기서 열린 포지션 전부 닫음
        csvfile = self.ticker+".csv"
        if self.longshort == 1:
            # close long
            self.binance_client.futures_create_order(symbol=self.ticker, side='SELL', type='MARKET', quantity=self.coin)
            print("closed-long")
            with open(csvfile, "a", newline="") as writecsv:
                wr = csv.writer(writecsv)
                wr.writerow([self.stdate, datetime.datetime.now(), self.avprice, price,
                             (price-self.avprice)*100/self.avprice, datetime.datetime.now()-self.stdate])
        elif self.longshort == 2:
            # close short
            self.binance_client.futures_create_order(symbol=self.ticker, side='BUY', type='MARKET', quantity=self.coin)
            print("closed-short")
            with open(csvfile, "a", newline="") as writecsv:
                wr = csv.writer(writecsv)
                wr.writerow([self.stdate, datetime.datetime.now(), self.avprice, price,
                             -(price-self.avprice)*100/self.avprice, datetime.datetime.now()-self.stdate])

    def terminate(self):
        super().terminate()
