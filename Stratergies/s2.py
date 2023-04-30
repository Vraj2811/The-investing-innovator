# The Accumulation/Distribution line (A/D line)

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from yahoo_fin.stock_info import get_data
import plotly.graph_objs as go

symbol = "RELIANCE"

symb = symbol+".NS"

data = get_data(symb, start_date="08/01/2018",
                end_date="08/31/2022", index_as_date=True, interval="1d")

def ad_line(data):
    adl = pd.Series(0.0, index=data.index)
    adl.iloc[0] = ((data['close'].iloc[0] - data['low'].iloc[0]) - (data['high'].iloc[0] - data['close'].iloc[0])) / (data['high'].iloc[0] - data['low'].iloc[0]) * data['volume'].iloc[0]
    for i in range(1, len(data)):
        if data['close'].iloc[i] > data['close'].iloc[i-1]:
            mf = ((data['close'].iloc[i] - data['low'].iloc[i]) - (data['high'].iloc[i] - data['close'].iloc[i])) / (data['high'].iloc[i] - data['low'].iloc[i]) * data['volume'].iloc[i]
        else:
            mf = ((data['close'].iloc[i] - data['high'].iloc[i]) - (data['low'].iloc[i] - data['close'].iloc[i])) / (data['high'].iloc[i] - data['low'].iloc[i]) * data['volume'].iloc[i]
        adl.iloc[i] = adl.iloc[i-1] + mf
    return adl

def AD_Line_trading_bot(data, portfolio=100000, stop_loss=0.05, commission=20):
    data['adl'] = ad_line(data)

    data['buy_signal'] = np.where(data['adl'] > data['adl'].shift(1), 1, 0)
    data['sell_signal'] = np.where(data['adl'] < data['adl'].shift(1), 1, 0)

    shares = 0
    trade_count = 0
    for i in range(1, len(data)):
        if data['sell_signal'].iloc[i] == 1:
            if shares > 0:
                portfolio += shares * data['close'].iloc[i] - commission
                shares = 0
                trade_count += 1

        if data['buy_signal'].iloc[i] == 1:
            if shares == 0:
                shares = portfolio // data['close'].iloc[i]
                portfolio -= shares * data['close'].iloc[i] + commission
                trade_count += 1

        if shares > 0 and data['close'].iloc[i] < (1 - stop_loss) * data['close'].iloc[0]:
            portfolio += shares * data['close'].iloc[i] - commission
            shares = 0
            trade_count += 1

    if shares > 0:
        portfolio += shares * data['close'].iloc[-1]
        final_portfolio = portfolio

    print("Final portfolio value: Rs. {0:.2f}".format(final_portfolio))
    print("Total trades: {0}".format(trade_count))

AD_Line_trading_bot(data)