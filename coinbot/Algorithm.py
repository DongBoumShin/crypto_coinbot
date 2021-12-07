import numpy as np
import pandas

import important_methods as meth


class Algorithm:
    def __init__(self, tickers):
        pass

    def buysell(self, data05, data15, data60, ticker, soldflag):
        raise NotImplementedError('obv')

    def _buysell(self, ticker) -> int:
        raise NotImplementedError('obv')

		

class ExampleAlg(Algorithm):
    def __init__(self, tickers):
        self.bought = {}
        self.hasflag = {}
        for ticker in tickers:
            self.bought[ticker] = False

    def buysell(self, data05, data15, data60, ticker, soldflag):
        self.data05 = data05
        self.data15 = data15
        self.data60 = data60
        self.curprice = self.data05.iat[-1, 4]

        res = self._buysell(ticker)
        if res == 1:
            target, stoploss, avprice, atr_var = self._set_trade_area_long()
            req_info = (target, stoploss, avprice, atr_var)
            self.hasflag[ticker] = res
            return 1, req_info
        elif res == 2:
            target, stoploss, avprice, atr_var = self._set_trade_area_short()
            req_info = (target, stoploss, avprice, atr_var)
            self.hasflag[ticker] = res
            return 2, req_info
        else:
            return 0, [1, 1, 1, 1]

    def _set_trade_area_short(self):
        atr_var = meth.atr(self.data05).iat[-1] #+ (self.curprice - self.data05.iat[-1, 3])
        curprice = self.data05.iat[-1, 4]
        mul=1
        if atr_var <= curprice*0.01:
            mul = 1.5
        target = curprice - 2.8*mul*atr_var
        stoploss = self.data05.iat[-1, 2] + 1*mul*atr_var
        avprice = curprice
        return target, stoploss, avprice, atr_var*mul

    def _set_trade_area_long(self):
        atr_var = meth.atr(self.data05).iat[-1] #+ (self.curprice - self.data05.iat[-1, 3])
        mul=1
        curprice = self.data05.iat[-1, 4]
        if atr_var <= curprice*0.01:
            mul = 1.5
        target = curprice + 2.8 * mul * atr_var
        stoploss = self.data05.iat[-1, 3] - 1*mul*atr_var
        avprice = curprice
        return target, stoploss, avprice, atr_var*mul

    def _buysell(self, ticker) -> int:
        sma22 = meth.ema(self.data05, 22)
        supertrend = meth.supertrend(self.data05)
        if not self.bought[ticker]:
            if supertrend['supertrend'].iat[-1]:
				if self.curprice > sma22.iat[-1]:
					self.bought[ticker] = True
					return 1
            elif not supertrend['supertrend'].iat[-1]:
				if self.curprice < sma22.iat[-1]:
					self.bought[ticker] = True
					return 2

