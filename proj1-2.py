import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st

def plot_label(start_date, end_date):
    btc = yf.download("BTC-USD", start=start_date, end=end_date)
    wall = 100
    wall2 = 100
    fig, ax = plt.subplots(figsize=(10, 6))

    if not btc.empty:
        x1 = [pd.Timestamp(start_date)]
        y1 = [wall]
        x2 = [pd.Timestamp(start_date)]
        y2 = [wall2]
        btc_open = pd.DataFrame(btc, columns=['Open'])
        
        btc_open['Date'] = btc_open.index.dayofweek
        saturdays = btc_open[btc_open['Date'] == 5]  
        saturdays = saturdays.drop(columns=['Date'])

        btc_close = pd.DataFrame(btc, columns=['Close', 'High'])
        
        btc_close['Date'] = btc_close.index.dayofweek
        wednesday = btc_close[btc_close['Date'] == 2]
        wednesday = wednesday.drop(columns=['Date'])

        first_sat = saturdays.index[0]
        first_wed = wednesday.index[0]

        if pd.Timestamp(first_sat) > pd.Timestamp(first_wed):
            wednesday = wednesday.drop(first_wed)

        last_sat = saturdays.index[-1]
        last_wed = wednesday.index[-1]

        if pd.Timestamp(last_sat) > pd.Timestamp(last_wed):
            saturdays = saturdays.drop(last_sat)

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
        
        ax.plot(x1, y1, label="Now", color="r")
        ax.plot(x2, y2, label="Ideal", color="b")
        ax.set_xlabel('Date')
        ax.set_ylabel('Wallet')
        ax.set_title('Business')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
    else:
        ax.text(0.5, 0.5, "Failed to download data.", ha='center')

    return fig

st.title("BTC Plot")

start_date_str = st.text_input("Start Date(YYYY-MM-DD)", value="")
end_date_str = st.text_input("End Date(YYYY-MM-DD)", value="")

if st.button("Show"):
    if start_date_str and end_date_str:
        try:
            start_date = pd.to_datetime(start_date_str).strftime('%Y-%m-%d')
            end_date = pd.to_datetime(end_date_str).strftime('%Y-%m-%d')
            fig = plot_label(start_date, end_date)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter valid start and end dates.")
