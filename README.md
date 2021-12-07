# crypto_coinbot
simple crypto trading bot for binance users

CryptoCurrency investing is more or less a gamble, and large sums of capital will be lost. None of the below, and any results you get from using this bot are in any form reliable financial advisements.

Use at your own risk, and I am not liable for any results this code might bring.

Although if you do have any success, could you kindly share your secrets with me?


* Known bugs
* * Rarely when the Controller sends an order to close a position, binance will reject the order. I do not know why this happens, as the bot correctly sends an order, and gets a correct return. As this bot nor the binance app sends alerts to your phone, the best bet is to check at least daily. I had this bug occur after about 3 weeks in, so maybe try rebooting your pc every week or so.


This bot operates on a 5min timeframe. Should you choose to move into lower timeframes, check your latency with the Binance servers. For me, it took about 100ms, which was absolutely terrible. So I opted for a higher timeframe.

This bot uses trailing stops and nothing else as exit points. That is, the algorithm only serves as entry points. It works good enough for me.

This bot uses Binance Futures, as they have the lowest futures fee and also provide long and short positions, along with leverages, if you're willing to risk it.

If you have seen my crypto simulator project, this works very similarly.

In fact, the only 2 differences are that the algorithm no longer manages exits, and that it stores 'hasflags' in a dictionary so no multiple positions are opened for any pair.

Algorithm now returns an integer flag of 0, 1, 2, along with a tuple of values required by the Controller. Example Algorithm is provided with guaranteed horrible returns.

Controller gets the returned required info, sets a stoploss and a target price, and opens the position accordingly.

When the position closes, a list is logged to a .csv file with the pair's name. Please run csvmaker.py before anything.

Binance user key and secret key are hard coded.

Maximum number of open position is 5, and leverage at 1, but feel free to adjust.

Press F11 key to close every position and exit.

For more info, please refer to my crypto_simulator project.

Again, use at your own risk.

PreReqs

Pandas, Numpy, Apscheduler, Psutil, Pynput, Python-Binance(binance)
