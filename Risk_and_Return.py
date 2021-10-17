# import modules

import pandas as pd
import yfinance as yf
from nsetools import Nse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import numpy as np
import plotly.express as px
from GoogleNews import GoogleNews


def get_stock_analysis(ticker, start_date, end_date):

    q = nse.get_quote(ticker)
    stock_df = yf.download(ticker+'.NS', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)['Close']
    nifty = yf.download('^NSEI', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)['Close']
    
    stock_df = stock_df.reset_index()
    stock_df['Returns'] = round(stock_df['Close'].pct_change(), 2)
    
    nifty = nifty.reset_index()
    nifty['Returns'] = round(nifty['Close'].pct_change(), 2)
    
    stock_df['Date'] = pd.to_datetime(stock_df['Date'], format="%Y-%m-%d")
    nifty['Date'] = pd.to_datetime(nifty['Date'], format="%Y-%m-%d")
    
    risk = round(np.std(stock_df['Returns'])*np.sqrt(250))
    returns = round((1 + stock_df['Returns'].mean())**250 - 1)
    beta = round(stock_df['Returns'].cov(nifty['Returns'])/np.var(nifty['Returns']), 2)
    
    return stock_df, risk, returns, beta, q.get('high52'), q.get('low52')

def get_latest_news(ticker):
    
    googlenews = GoogleNews(period='7d', lang = 'en')
    googlenews.search(f'intitle:{tickers.get(ticker)}')
    result=googlenews.result()
    df=pd.DataFrame(result)
    df.sort_values('datetime', inplace=True)
    df = df.head(10).reset_index(drop=True)
    df['Latest News'] = '<a href=' + df['link'] + '>' + df['desc'] + '</a>'
    #tbl = pd.DataFrame(df['Latest News']).to_html(escape=False, index=False).replace("right", "center")
    return df
    
def create_app(tickers):
    st.set_page_config(page_title='Stock Analysis', layout='wide')
    st.markdown("<h2 style='text-align: center; color: black;'>Financial Analysis</h2>", unsafe_allow_html=True)
    ticker = st.sidebar.selectbox('Select ticker', tickers)
    year = st.sidebar.slider('Select years', 0, 15)
    if year and ticker:
        st.markdown(f"<p style='text-align: center; color: black;'>{tickers.get(ticker)}</p>", unsafe_allow_html=True)
        
        stock_df, risk, returns, beta, high52, low52 = get_stock_analysis(ticker, datetime.now()-relativedelta(years=year), datetime.now())
        df = get_latest_news(ticker)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric('Annualized Risk (%)', risk*100)
        col2.metric('Annualized Returns (%)', returns*100)
        col3.metric('Beta', beta)
        col4.metric('52 weeks high', high52)
        col5.metric('52 weeks low', low52)
        
        fig1 = px.line(stock_df,x="Date", y="Close", width=1200, height=500)
        st.plotly_chart(fig1)
        
        st.markdown(f'''
                        | Latest News |
                        | :------: |
                        | {df['Latest News'][0]}| 
                        | {df['Latest News'][1]} | 
                        | {df['Latest News'][2]} |
                        | {df['Latest News'][3]} |
                        | {df['Latest News'][4]} |
                        ''', unsafe_allow_html=True)
    
if __name__=="__main__":
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    tickers = dict(reversed(list(all_stock_codes.items())))
    create_app(tickers)
    
    
    
    

