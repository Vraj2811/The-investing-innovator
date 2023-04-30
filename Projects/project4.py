'''
CANDLESTICK GRAPH OF A GIVEN STOCK OF EVERY DAY IN LAST 1 YEAR
'''

import pandas as pd
from datetime import date, timedelta
from nsepy import get_history
from nsetools import Nse
import plotly.graph_objs as go

nse=Nse()
symbol="ADANIENT"

start_date = date.today() - timedelta(days=365)
end_date = date.today()
data = get_history(symbol=symbol, start=start_date, end=end_date)

fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title=f'{symbol} live share price evolution',
    yaxis_title='Stock Price (INR per Shares)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=3, label="3 month", step="month", stepmode="backward"),
            dict(count=6, label="6 month", step="month", stepmode="backward"),
            dict(count=9, label="9 month", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()