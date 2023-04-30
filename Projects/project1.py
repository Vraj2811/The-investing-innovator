'''
In this project, we will extract the latest data of all the stocks listed in the NSE.
Also find the no. of shares to buy if each stock should be given equal amount
'''

from nsetools import Nse
import pandas as pd

nse=Nse()

stocks=list(nse.get_stock_codes(cached=False))

my_columns=['Ticker','Latest Price','No. of shares to buy']
finalDB=pd.DataFrame(columns=my_columns)

tot=10000000

for i in range(1,len(stocks)):
    symbol=stocks[i]
    try:
        a=nse.get_quote(symbol)
        p=a['lastPrice']
        x=pd.DataFrame([[symbol,p,int(tot/(len(stocks)*p))]],columns=my_columns)
        finalDB=pd.concat([finalDB,x],ignore_index=True)

    except IndexError:
        continue

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

print(finalDB)