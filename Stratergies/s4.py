# The Stochastic Oscillator

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

def SO_trading_bot(df, portfolio_value=100000, stop_loss=0.05, commission=20):
    window_length = 14
    high = df['high'].rolling(window_length).max()
    low = df['low'].rolling(window_length).min()
    k = 100 * (df['close'] - low) / (high - low)
    d = k.rolling(3).mean()

    position = 0
    trade_count = 0

    for i in range(len(df)):
        price = df['close'][i]
        k_val = k[i]
        d_val = d[i]

        if k_val < 20 and d_val < 50 and position == 0:
            shares_to_buy = np.floor(portfolio_value / price)
            cost = shares_to_buy * price
            portfolio_value -= cost
            portfolio_value-=commission
            position = shares_to_buy
            trade_count += 1

        elif k_val > 80 and d_val > 50 and position > 0:
            sale_price = price * position
            portfolio_value += sale_price
            portfolio_value-=commission
            position = 0
            trade_count += 1

        elif position > 0 and price < (1 - stop_loss) * df['close'][i-1]:
            sale_price = price * position
            portfolio_value += sale_price
            portfolio_value-=commission
            position = 0
            trade_count += 1

    print(f'Final portfolio value: Rs. {portfolio_value:.2f}')
    print("Total trades: {0}".format(trade_count))

SO_trading_bot(data)