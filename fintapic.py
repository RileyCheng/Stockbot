import math
from finta import TA as ta
import pandas as pd
import yfinance as yf
import numpy as np
import os
import datetime

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

def F():
    ticker = "2330.TW"
    df = yf.download(ticker,"2020-01-01")

    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['up_down']=np.where(data['Adj Close'] >= data['Adj Close'].shift(1), 1, -1)

    bbands = ta.BBANDS(df, 30)
    data['bbandsU'] = bbands.BB_UPPER
    data['bbandsL'] = bbands.BB_LOWER
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)

    data = data.dropna(axis=0, how='any')

    fig = go.Figure()
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01, 
                        row_heights=[0.5,0.1,0.2,0.2,0.2])
    # 1st row
    fig.add_trace(go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'], 
                                showlegend=False))
    # add moving average traces
    fig.add_trace(go.Scatter(x=data.index, 
                            y=data['MA5'], 
                            opacity=0.7, 
                            line=dict(color='#2894FF', width=2), 
                            name='5日均線'))
    fig.add_trace(go.Scatter(x=data.index, 
                            y=data['MA10'], 
                            opacity=0.7, 
                            line=dict(color='orange', width=2), 
                            name='10日均線'))

    # 2nd row
    colors = ['green' if row['Open'] - row['Close'] >= 0 
            else 'red' for index, row in data.iterrows()]
    fig.add_trace(go.Bar(x=data.index, 
                        y=data['Volume'],
                        marker_color=colors,
                        name='成交量',
                        showlegend=False
                        ), row=2, col=1)
    # 3rd row
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['k'],
                            line=dict(color='#E6AECF', width=2),
                            name='K線'
                            ), row=3, col=1)
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['d'],
                            line=dict(color='#7F9871', width=2),
                            name='D線'
                            ), row=3, col=1)
    # 4th row
    colors = ['green' if val >= 0 
            else 'red' for val in data['DIF-MACD']]
    fig.add_trace(go.Bar(x=data.index, 
                        y=data['DIF-MACD'],
                        marker_color=colors,
                        name='DIF-MACD',
                        showlegend=False
                        ), row=4, col=1)
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['DIF'],
                            line=dict(color='#A299CA', width=2),
                            name='快線DIF'
                            ), row=4, col=1)
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['MACD'],
                            line=dict(color='#FFA289', width=2),
                            name='慢線MACD'
                            ), row=4, col=1)

    # 5th row
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['RSI10'],
                            line=dict(color='#01ACBD', width=2),
                            name='10日RSI'
                            ), row=5, col=1)

    # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
    fig.update_layout(height=900, width=1000, 
    #                   showlegend=False, 
                    xaxis_rangeslider_visible=False)

    # update y-axis label
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="KD", row=3, col=1)
    fig.update_yaxes(title_text="MACD", row=4, col=1)
    fig.update_yaxes(title_text="RSI", row=5, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)
    # add chart title 
    fig.update_layout(title=stock)

    # removing white space
    fig.update_layout(margin=go.layout.Margin(
            l=20, #left margin
            r=20, #right margin
            b=20, #bottom margin
            t=30  #top margin
        ))

    pic = fig.show()
    graphJSON = json.dumps(pic, cls=py.utils.PlotlyJSONEncoder)

    return render_template('p.html', graphJSON=graphJSON)
