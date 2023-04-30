import pandas as pd
import numpy as np
from datetime import date, timedelta
from nsepy import get_history
import matplotlib.pyplot as plt

# Download historical data for a stock or ETF
symbol = 'ADANIENT'
start_date = date.today() - timedelta(days=365)
end_date = date.today()
data = get_history(symbol=symbol, start=start_date, end=end_date)

# Define the window and number of standard deviations for the Bollinger Bands
window = 20
num_std = 2

data["Typical Price"]=(data["Low"]+data["High"]+data["Close"])/3

# Calculate the rolling mean and standard deviation
rolling_mean = data['Typical Price'].rolling(window=window).mean()
rolling_std = data['Typical Price'].rolling(window=window).std()

# Calculate the upper and lower Bollinger Bands
upper_band = rolling_mean + (rolling_std * num_std)
lower_band = rolling_mean - (rolling_std * num_std)

# Plot the data and Bollinger Bands
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='Price')
plt.plot(upper_band, label='Upper Band')
plt.plot(lower_band, label='Lower Band')
plt.legend()
plt.title('Bollinger Bands for ' + symbol)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
