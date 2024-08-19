import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def check_value(row):
    global wall_1
    if not pd.isna(row['Close']):
        btc_amount = float(0)
        final = float(0)
        res = float(0)
        btc_amount = wall_1 / row['Open']
        final = btc_amount * row['Close']
        res = final - wall_1
        wall_1 = final
        return wall_1
    return wall_1


btc = yf.download("BTC-USD", start="2019-1-1", end="2024-8-5")
wall_1 = 1000

btc['Date'] = btc.index

btc_df = pd.DataFrame(btc, columns=['Date', 'Open', 'Close'])

# btc_df.to_csv("F:\\DA\\Projects\\btc_csv.csv")


btc_df['Date1'] = btc_df.index.dayofweek

btc_df = btc_df.loc[(btc_df['Date1'] == 2) | (btc_df['Date1'] == 5)] #saturday = 5

if btc_df.iloc[0]['Date1'] == 2:
    btc_df = btc_df.drop(btc_df.index[0])
# print(btc_df)


# btc_df.drop(['Date1'], axis = 1, inplace = True)
btc_df['Close'] = btc_df['Close'].shift(-1)
# print(btc_df)

btc_df = btc_df.loc[(btc_df['Date1'] == 5)]


btc_df['result'] = btc_df.apply(check_value, axis = 1)

plt.figure(figsize=(12, 6))
plt.plot(btc_df['Date'], btc_df['result'], marker='o', linestyle='-', color='b')
plt.xlabel('Date')
plt.ylabel('Result')
plt.title('Result vs Date')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Balance : 1000.0$")
print("Now : ", int(wall_1), "$")

btc_df.to_csv("F:\\DA\\Projects\\btc_csv3.csv")