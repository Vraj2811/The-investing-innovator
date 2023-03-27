'''
MAILNLY FOR LONG TERM INVESTING
In this project, we will find top 50 companies with maximum 1 year return.
Also will find the no. of shares to buy if each stock should be given equal amount.
'''

import pandas as pd
from datetime import date, timedelta
from nsepy import get_history
from nsetools import Nse

nse=Nse()

stocks=list(nse.get_stock_codes(cached=False))

my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']

finalDB=pd.DataFrame(columns=my_columns)

tot=10000000

for i in range(1,len(stocks)):
    symbol=stocks[i]
    try:        
        start_date = date.today() - timedelta(days=365)
        end_date = date.today()
        df = get_history(symbol=symbol, start=start_date, end=end_date)
        open_price = df.iloc[0]['Open']
        close_price = df.iloc[-1]['Close']
        one_year_return = (close_price - open_price) / open_price*100

        a=nse.get_quote(symbol)    
        p=a['lastPrice']

        x=pd.DataFrame([[symbol,p,one_year_return,0]],columns=my_columns)
        finalDB=pd.concat([finalDB,x],ignore_index=True)

    except IndexError:
        print("")

finalDB.sort_values('One-Year Price Return',ascending=False,inplace=True)
finalDB=finalDB[:50]
finalDB.reset_index(inplace=True)
del finalDB['index']

for i in range(len(finalDB)):
    finalDB.loc[i,'Number of Shares to Buy']=int(tot/(len(finalDB)*finalDB.loc[i,'Price']))

print(finalDB)