import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

btc = yf.download("BTC-USD", start="2019-1-1", end="2024-8-5")
wall = 100
wall2 = 100

if not btc.empty:
    x1 = [pd.Timestamp("2019-1-1")]
    y1 = [wall]
    x2 = [pd.Timestamp("2019-1-1")]
    y2 = [wall2]
    btc_open = pd.DataFrame(btc, columns=['Date', 'Open'])
    
    btc_open['Date'] = btc_open.index.dayofweek
    saturdays = btc_open[btc_open['Date'] == 5]  
    saturdays = saturdays.drop(columns=['Date'])

    btc_close = pd.DataFrame(btc, columns=['Date', 'Close', 'High'])
    
    btc_close['Date'] = btc_close.index.dayofweek
    wednesday = btc_close[btc_close['Date'] == 2]
    wednesday = wednesday.drop(columns=['Date'])

    first_sat = saturdays.index[0]
    first_wed = wednesday.index[0]

    if pd.Timestamp(first_sat) > pd.Timestamp(first_wed):
        wednesday.drop(first_wed, inplace=True)


    last_sat = saturdays.index[-1]
    last_wed = wednesday.index[-1]

    if pd.Timestamp(last_sat) > pd.Timestamp(last_wed):
        saturdays.drop(last_sat, inplace=True)

    for (sat_index, sat_row), (wed_index, wed_row) in zip(saturdays.iterrows(), wednesday.iterrows()):
        timestamp = pd.Timestamp(sat_index)
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        x1.append(f"{year}-{month:02d}-{day:02d}")
        wall -= sat_row['Open']
        wall += wed_row['Close']
        y1.append(wall)

    for (sat_index, sat_row), (wed_index, wed_row) in zip(saturdays.iterrows(), wednesday.iterrows()):
        timestamp = pd.Timestamp(sat_index)
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        x2.append(f"{year}-{month:02d}-{day:02d}")
        wall2 -= sat_row['Open']
        wall2 += wed_row['High']
        y2.append(wall2)
    

    
    plt.plot(x1, y1, label="Now", color= "r")
    plt.plot(x2, y2, label="Ideal", color= "b")
    plt.xlabel('Date')
    plt.ylabel('Wallet')
    plt.title('Bussines')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Failed to download data.")