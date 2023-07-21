import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import talib
import os
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas as pd
import json
import pymysql
from flask import Flask, render_template
app = Flask(__name__)
@app.route("/picture")
def picture(): 
    conn = pymysql.connect(
    host='us-cdbr-east-05.cleardb.net',
    user='be59caf2e81229',
    password='75242529',
    db='heroku_da386d83e593c1d',
    charset='utf8'
)   
    engine = create_engine("mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net/heroku_da386d83e593c1d")
    sql = '''
        select * from stock_daily WHERE id=1101;
        ''' 
    df = pd.read_sql_query(sql, engine)

    date="2021-12-26"
    date = pd.to_datetime(date)
    mask = (df['Date'] >= date)

    data=pd.DataFrame()
    data['id']=df.loc[mask]['id']
    data['Date']=df.loc[mask]['Date']
    data['Open']=df.loc[mask]['Open']
    data['High']=df.loc[mask]['High']
    data['Low']=df.loc[mask]['Low']
    data['Close']=df.loc[mask]['Close']
    data['Volume']=df.loc[mask]['Volume']

    data['MA5'] = talib.MA(df.loc[mask]['Close'], timeperiod=5)
    data['MA10'] = talib.MA(df.loc[mask]['Close'], timeperiod=10)
    data['MA20'] = talib.MA(df.loc[mask]['Close'], timeperiod=20)
    data['MA60'] = talib.MA(df.loc[mask]['Close'], timeperiod=60)
    data['k'], data['d'] = talib.STOCH(df.loc[mask]['High'], df.loc[mask]['Low'], df.loc[mask]['Close'])
    data['RSI5']=talib.RSI(df.loc[mask]['Close'],timeperiod=5)
    data['RSI10']=talib.RSI(df.loc[mask]['Close'],timeperiod=10)
            # MACD快線、MACDSIGNAL慢線、MACDHIST快線-慢線(柱狀圖)
    data['DIF'],data['MACD'],data['DIF-MACD'] = talib.MACD(df.loc[mask]['Close'],fastperiod=12, slowperiod=26, signalperiod=9)
    data.index = pd.DatetimeIndex(df.loc[mask]['Date'])

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
                                    y=data['MA20'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='20日均線'))

            # 2nd row
    colors = ['red' if row['Open'] - row['Close'] >= 0 
                    else 'green' for index, row in data.iterrows()]
    fig.add_trace(go.Bar(x=data.index, 
                                y=data['Volume'],
                                marker_color=colors,
                                name='成交量',
                                showlegend=False
                                ), row=2, col=1)

    data2=[fig.show()]
    graphJSON = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder) 
        
    conn.close()     

    return render_template('picture.html',graphJSON=graphJSON)
if __name__ == '__main__':
    app.debug = True
    app.run()