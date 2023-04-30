# Parabolic SAR

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


def Parabolic_SAR_trading_bot(df, portfolio_value=100000, stop_loss=0.05, commission=20):
    trade_count = 0

    af = 0.02
    max_af = 0.2
    prev_sar = df['low'][0]
    prev_ep = df['high'][0]
    prev_af = af
    sar_values = [prev_sar]

    for i in range(1, len(df)):
        curr_high = df['high'][i]
        curr_low = df['low'][i]
        curr_sar = prev_sar + prev_af * (prev_ep - prev_sar)

        if curr_sar > curr_low:
            curr_sar = curr_low
        elif curr_sar < prev_ep:
            curr_sar = prev_ep

        if curr_high > prev_ep:
            curr_ep = curr_high
            curr_af = min(prev_af + af, max_af)
        else:
            curr_ep = prev_ep
            curr_af = prev_af

        sar_values.append(curr_sar)

        prev_sar = curr_sar
        prev_ep = curr_ep
        prev_af = curr_af

    df['SAR'] = sar_values

    position = 0

    for i in range(len(df)):
        price = df['close'][i]
        sar_val = df['SAR'][i]

        if price > sar_val and position == 0:
            shares_to_buy = np.floor(portfolio_value / price)
            cost = shares_to_buy * price
            portfolio_value -= cost
            portfolio_value -= commission
            position = shares_to_buy
            trade_count += 1

        elif price < sar_val and position > 0:
            sale_price = price * position - 20
            portfolio_value += sale_price
            portfolio_value -= commission
            position = 0
            trade_count += 1

        elif position > 0 and price < (1 - stop_loss) * df['close'][i-1]:
            sale_price = price * position - 20
            portfolio_value += sale_price
            trade_count += 1
            portfolio_value -= commission
            position = 0
    portfolio_value += (position * data['close'][-1])
    print(f'Final portfolio value: Rs. {portfolio_value:.2f}')
    print("Total trades: {0}".format(trade_count))


Parabolic_SAR_trading_bot(data)
