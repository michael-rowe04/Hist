import pandas as pd
import yfinance as yf
from datetime import datetime

#Just run this file to update the csvs for making the barchart data
#These csvs contain the close data for all the stocks in the specified csv


def down_data(column_name):
    stocks = pd.read_csv('my_csvs/stock_categories.csv')
    #column_name = 'S&P'
    non_nan_tickers = list(stocks[stocks[column_name].notna()][column_name])
    the_data = yf.download(non_nan_tickers)

    return the_data

def make_csv(the_data,column_name):
    dropped = the_data.drop(columns = ['Adj Close','High','Low','Open']) 
    #the_data.columns = the_data.columns.swaplevel(0, 1)
    dropped.columns = ['_'.join(map(str, col)) for col in dropped.columns]
    dropped.to_csv('my_csvs/'+column_name+".csv")


def make_update(column_name):
    """Update the csvs with all the stocks OCLHV
    
    column_name (str): Column name for stock_categories. I.e. NASDAQ100,S&PRealEstate, etc."""
    the_data = down_data(column_name)
    make_csv(the_data,column_name)
    with open('my_csvs/update.txt','w') as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(current_time)


csv = pd.read_csv('my_csvs/stock_categories.csv')
for col in csv.columns:
    #make_csv(down_data(col),col)
    make_update(col)