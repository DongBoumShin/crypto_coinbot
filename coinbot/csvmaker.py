import csv

tiers = [['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'LTCUSDT', 'ETCUSDT'],
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
for ticker in tickers:
    csvfile = ticker+".csv"

with open(csvfile, "w", newline="") as writecsv:
	wr = csv.writer(writecsv)
	wr.writerow(["stdate", "enddate", "stprice", "endprice",
				 "percentage", "elapsed"])
