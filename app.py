# streamlit stock price app

import yfinance as yf
import streamlit as st
import pandas as pd
import datetime

st.write("""
# Streamlit Stock Price App

Enter a stock ticker to see price data over time. 
  * Get daily Open, High, Low, Close, and Volume.
* You can download the data to use in your own projects. Data via [yfinance](https://pypi.org/project/yfinance/).

**Try it out:** Enter NKE to get NIKE, Inc. stock price data over a selected timeframe.

""")

# input the stock ticker
ticker = st.text_input('Enter a Stock Ticker Symbol', 'Ex. GOOGL')

# get the data for this ticker
ticker_data = yf.Ticker(ticker)

# define start and end dates
start_date = st.date_input(
    "Enter Start Date",
    datetime.date(2008, 1, 1))

end_date = st.date_input(
    "Enter End Date",
    datetime.date(2022, 3, 17))

# get prices over time for the ticker into a dataframe
ticker_df = ticker_data.history(
    period='1d', start=start_date, end=end_date)
# This data frame has columns:
# Open High Low Close Volume Dividends Stock-Splits

if ticker_df.empty:
    st.write('Please enter a valid ticker symbol')
else:
    # Drop the Dividends and Stock-Splits columns
    ticker_df = ticker_df.drop(columns=['Dividends', 'Stock Splits'])

    # get the company name from the ticker entered
    company_name = ticker_data.info['longName']

    # Display data table
    st.write('## ' + company_name + ' Data Table')
    st.table(ticker_df.head())

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    # convert the ticker dataframe to csv for download
    csv = convert_df(ticker_df)

    # create the download button for users to grab the stock price data
    download_button_label = f'Download {company_name} data as CSV'
    st.download_button(
        label=download_button_label,
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

    # Display the Daily Closing Price data
    st.write('## ' + company_name + ' Daily Closing Price')
    st.line_chart(ticker_df.Close)

    # Display the Daily Volume dataa
    st.write('## ' + company_name + ' Daily Volume')
    st.bar_chart(ticker_df.Volume)
