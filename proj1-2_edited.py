import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as slt


def check_value(row):
    global wall_1
    if not pd.isna(row['Close']):
        btc_amount = wall_1 / row['Open']
        final = btc_amount * row['Close']
        res = final - wall_1
        wall_1 = final
        return wall_1
    return wall_1
wall_1 = 1000
def plt_web(s, e):
    btc = yf.download("BTC-USD", start=s, end=e)
    
    wall_2 = 1000

    btc['Date'] = btc.index

    btc_df = pd.DataFrame(btc, columns=['Date', 'Open', 'Close'])

    # btc_df.to_csv("F:\\DA\\Projects\\btc_csv.csv")


    btc_df['Date1'] = btc_df.index.dayofweek

    btc_df = btc_df.loc[(btc_df['Date1'] == 2) | (btc_df['Date1'] == 5)] #saturday = 5

    if btc_df.iloc[0]['Date1'] == 2:
        btc_df = btc_df.drop(btc_df.index[0])
    # print(btc_df.columns)


    btc_df.drop(['Date1'], axis = 1, inplace = True)
    btc_df['Close'] = btc_df['Close'].shift(-1)
    # print(btc_df)


    btc_df['result'] = btc_df.apply(check_value, axis = 1)

    plt.figure(figsize=(12, 6))
    plt.plot(btc_df['Date'], btc_df['result'], marker='o', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Result')
    plt.title('Result vs Date')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # plt.show()
    return plt

    # print("Balance : 1000.0$")
    # print("Now : ", wall_1, "$")

    # btc_df.to_csv("F:\\DA\\Projects\\btc_csv2.csv")


slt.title("BTC Plot")

start_date_str = slt.text_input("Start Date(YYYY-MM-DD)", value="")
end_date_str = slt.text_input("End Date(YYYY-MM-DD)", value="")

if slt.button('Show'):
    if start_date_str and end_date_str:
        start_date = pd.to_datetime(start_date_str).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date_str).strftime('%Y-%m-%d')
        fig = plt_web(start_date, end_date)
        slt.pyplot(fig)
        slt.write("Balance : 1000.0$")
        slt.write("Now : ", wall_1, "$")
    else:
        st.error("Please enter valid start and end dates.")
