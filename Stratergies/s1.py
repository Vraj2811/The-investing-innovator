# The On-Balance-volume indicator (OBV)

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


def OBV_trading_bot(data, initial_portfolio=100000, stop_loss=0.05, commission=20):

    shares_owned = 0
    cash = initial_portfolio
    buy_price = 0
    sell_price = 0
    stop_loss_price = 0
    trade_count = 0

    data['OBV'] = np.where(data['close'] > data['close'].shift(1), data['volume'],
                           np.where(data['close'] < data['close'].shift(1), -data['volume'], 0)).cumsum()

    for i in range(1, len(data)):

        if data['OBV'][i] > data['OBV'][i-1] and cash > 0:
            shares_to_buy = cash // (data['close'][i] + commission)
            buy_price = data['close'][i]
            shares_owned += shares_to_buy
            cash -= shares_to_buy * buy_price
            cash -= commission
            trade_count += 1
            stop_loss_price = buy_price - (buy_price * stop_loss)
            print(f'Buy {shares_to_buy} shares at Rs. {buy_price:.2f}')

        elif data['OBV'][i] < data['OBV'][i-1] and shares_owned > 0:
            print(f'Sell {shares_owned} shares at Rs. {sell_price:.2f}')
            sell_price = data['close'][i]
            cash += shares_owned * sell_price
            cash -= commission
            trade_count += 1
            shares_owned = 0
            stop_loss_price = 0

        elif data['close'][i] < stop_loss_price and shares_owned > 0:
            print(f'Sell {shares_owned} shares at Rs. {sell_price:.2f}')
            sell_price = stop_loss_price
            cash += shares_owned * sell_price
            cash -= commission
            trade_count += 1
            shares_owned = 0
            stop_loss_price = 0

    final_portfolio = cash + (shares_owned * data['close'][-1])
    print(f'Final portfolio value: Rs. {final_portfolio:.2f}')
    print("Total trades: {0}".format(trade_count))


OBV_trading_bot(data)
