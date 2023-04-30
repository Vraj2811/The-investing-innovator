'''
MAILNLY FOR LONG TERM INVESTING
In this project, we will find top 50 companies with maximum HQM score.
HQM -> High Quality Momentum
Also find the no. of shares to buy if each stock should be given equal amount.
'''

import pandas as pd
from datetime import date, timedelta
from nsepy import get_history
from nsetools import Nse
from scipy import stats
from statistics import mean

nse=Nse()

stocks=list(nse.get_stock_codes(cached=False))[:5]

my_columns = [  'Ticker', 
                'Price', 
                'Number of Shares to Buy', 
                'One-Year Price Return', 
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score']

finalDB=pd.DataFrame(columns=my_columns)

tot=10000000

for i in range(1,len(stocks)):
    symbol=stocks[i]
    try:        
        end_date = date.today()
        start_date = date.today() - timedelta(days=365)
        df = get_history(symbol=symbol, start=start_date, end=end_date)
        one_year_return = (df.iloc[-1]['Close'] - df.iloc[0]['Open']) / df.iloc[0]['Open']*100

        start_date = date.today() - timedelta(days=183)
        df = get_history(symbol=symbol, start=start_date, end=end_date)
        six_month_return = (df.iloc[-1]['Close'] - df.iloc[0]['Open']) / df.iloc[0]['Open']*100

        start_date = date.today() - timedelta(days=30)
        df = get_history(symbol=symbol, start=start_date, end=end_date)
        one_month_return = (df.iloc[-1]['Close'] - df.iloc[0]['Open']) / df.iloc[0]['Open']*100

        a=nse.get_quote(symbol)    
        p=a['lastPrice']

        x=pd.DataFrame([[symbol,p,0,one_year_return,0,six_month_return,0,one_month_return,0,0]],columns=my_columns)
        finalDB=pd.concat([finalDB,x],ignore_index=True)

    except IndexError:
        print("")

time_periods = ['One-Year',
                'Six-Month',
                'One-Month']

for row in finalDB.index:
    for time_period in time_periods:
        finalDB.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(finalDB[f'{time_period} Price Return'], finalDB.loc[row, f'{time_period} Price Return'])

for row in finalDB.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(finalDB.loc[row, f'{time_period} Return Percentile'])
    finalDB.loc[row, 'HQM Score'] = mean(momentum_percentiles)

finalDB.sort_values('HQM Score', ascending = False,inplace='True')
finalDB=finalDB[:50]
finalDB.reset_index(inplace=True)
del finalDB['index']

for i in range(len(finalDB)):
    finalDB.loc[i,'Number of Shares to Buy']=int(tot/(len(finalDB)*finalDB.loc[i,'Price']))

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

print(finalDB)