from __future__ import unicode_literals
from crypt import methods
import os
from struct import pack

from sqlalchemy import create_engine
from flask import Flask, request, abort, render_template, redirect, flash, url_for

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

import configparser
import wei
import m1, m2, m3, sb1

#分頁
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
# crawler package
import requests
from bs4 import BeautifulSoup
import urllib
import re
import random

import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import json
from json import dumps as json_dumps
import yfinance as yf
import math
from finta import TA as ta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# import pandas_ta as ta

#database
from flask_sqlalchemy import SQLAlchemy
import pymysql
# import mysql.connector
from backtesting import Backtest, Strategy #引入回測和交易策略功能
from backtesting.lib import crossover #從lib子模組引入判斷均線交會功能
from backtesting.test import SMA #從test子模組引入繪製均線功能
import numpy as np
import pandas as pd
import datetime

config = configparser.ConfigParser()
config.read('config.ini')
#db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net/heroku_da386d83e593c1d"
db = SQLAlchemy(app)
conn = pymysql.connect(
    host='us-cdbr-east-05.cleardb.net',
    user='be59caf2e81229',
    password='75242529',
    db='heroku_da386d83e593c1d',
    charset='utf8'
)
class Bargain(db.Model):
  __tablename__ = 'bargain'
  id = db.Column(db.Integer)
  b_date = db.Column(db.Text,primary_key=True)
  f_investor = db.Column(db.Integer)
  trust = db.Column(db.Text)
  dealer = db.Column(db.Text)
  lending = db.Column(db.Text)
  borrowing = db.Column(db.Text)
  
class Income(db.Model):
  __tablename__ = 'income_statement'
  id = db.Column(db.Text)
  quarter = db.Column(db.Text,primary_key=True)
  income = db.Column(db.Text)
  cost = db.Column(db.Text)
  gross_profit = db.Column(db.Text)
  operating_expenses = db.Column(db.Text)
  operating_profit = db.Column(db.Text)
  Non_operating_income = db.Column(db.Text)
  profit_before_tax = db.Column(db.Text)
  profit_after_tax = db.Column(db.Text)
  
class Balance(db.Model):
  __tablename__ = 'balance_sheet'
  id = db.Column(db.Text)
  quarter = db.Column(db.Integer,primary_key=True)
  asset = db.Column(db.Text)
  liability = db.Column(db.Text)
  stockholder_equity = db.Column(db.Text)
  
class Finance(db.Model):
  __tablename__ = 'financial_ratio'
  quarter = db.Column(db.Text,primary_key=True)
  id = db.Column(db.Text)
  F2 = db.Column(db.Text)
  F3 = db.Column(db.Text)
  F5 = db.Column(db.Text)
  F7 = db.Column(db.Text)
  F8 = db.Column(db.Text)
  F9 = db.Column(db.Text)
  F27 = db.Column(db.Text)
  F51 = db.Column(db.Text)
class I1(db.Model):
  __tablename__ = 'stock_year'
  id = db.Column(db.Text)
  Dividends = db.Column(db.Text)#歷年股利
  d_yield= db.Column(db.Text) #殖利率
  capital = db.Column(db.Text) #股本
  Date=db.Column(db.Date,primary_key=True)
  
class I2(db.Model):
  __tablename__ = 'stock_pe'
  id = db.Column(db.Text)
  q= db.Column(db.Text,primary_key=True)#季度
  pe= db.Column(db.Float) #本益比
   
class I3(db.Model):
  __tablename__ = 'stock_value'
  id = db.Column(db.Text)
  quarter= db.Column(db.Text,primary_key=True)#季
  market_value= db.Column(db.Text) #市值

# stock_name
def s_name(id):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from stock where id= '  + str(id)
    cursor.execute(select)
      
    message = []
    message.extend(cursor.fetchall())

    cursor.close()
    conn.close()
    return message
#分頁
# mod = Blueprint('message2', __name__)
# finance
def finance(id):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from income_statement where id= '  + str(id)
    cursor.execute(select)
    message = []
    message.extend(cursor.fetchmany(4))

    cursor.close()
    conn.close()
    return message

def finance2(id):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from balance_sheet where id= '  + str(id)
    cursor.execute(select)
    message = []
    message.extend(cursor.fetchmany(4))

    cursor.close()
    conn.close()
    return message

def finance3(id):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from financial_ratio where id= '  + str(id)
    cursor.execute(select)
    message = []
    message.extend(cursor.fetchmany(4))

    cursor.close()
    conn.close()
    return message

# bargain
def bargain():
    conn = pymysql.connect(
    host='us-cdbr-east-05.cleardb.net',
    user='be59caf2e81229',
    password='75242529',
    db='heroku_da386d83e593c1d',
    charset='utf8'
  )
    cursor = conn.cursor()
    page=request.args.get(get_page_parameter(),type=int,default=1)
    limit=10
    offset=page*limit-limit
    # select = 'select * from bargain where id = ' + str(id)
    select = 'select * from bargain where id = 1101'
    cursor.execute(select)     
    message2 = []
    message2.extend(cursor.fetchall())
    total=len(message2)
    cur=conn.cursor()
    cur.execute("select * from bargain where id = 1101 limit %s offset %s",(limit,offset))
    data=cur.fetchall()
    cursor.close()
    conn.close()
    pagination=Pagination(page=page,per_page=limit,total=total,record_name='bargain')
    return message2,pagination,data
    
# news     
def news1():
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from news'
    cursor.execute(select)     
    message2 = []
    message2.extend(cursor.fetchmany(20))
    cursor.close()
    conn.close()

    return message2

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 網頁
@app.route("/")
def index():
    # Create data
    db.create_all()
    return 'ok'

#搜尋
#搜尋
# , methods=['GET', 'POST']
@app.route("/search")
def search():
  submit_btn = request.args.get("submit")
  print("submit_btn")
  if submit_btn != None:
    stock = request.args.get("search")
    print("search_value",stock)
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    cursor.execute(f"SELECT id,company from stock where id = '{stock}'")                      
    conn.commit()
    data = cursor.fetchall()
    data = data[0] if len(data) else 0
    # For text
    if data == 0 : 
      cursor.execute(f"SELECT id,company from stock where company like '%{stock}%'")
      conn.commit()
      data = cursor.fetchall()
      data = data[0] if len(data) else 0
      cursor.close()
      conn.close()
    
    print(data)
    if data == 0:
      data = ('NULL','無此公司')
      return render_template('search.html', id=data[0], company=data[1])
    else:
      return redirect(url_for('income',id=data[0]))
    
#搜尋新聞
# , methods=['GET', 'POST']
@app.route("/searchnews")
def searchnews():
  submit_btn = request.args.get("submitnews")
  if submit_btn != None:
    stock = request.args.get("searchnews")
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()

    cursor.execute(f"SELECT * from news where id = '{stock}'")                       
    conn.commit()
    # 產出 tuple
    data = cursor.fetchall()
    data= list(data)
    # [(1001,),(1101,)]
    cursor.close()
    conn.close()
    new_item = []
    for data in data:
      data=list(data)
      new_item.append(data)
    return render_template("searchnews.html",new_item=new_item)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/choose")
def choose():
    s = sb1.fin()
    return render_template("choose.html", stock = s)
  
# @app.route("/choose/<path:master>")
# def master(master):
#   if master == 'pe':
#     p = m2.fin()
#     return render_template("master/pe.html", master=master, pe = p)
#   elif master == 'bu':
#     b = m1.fin()
#     return render_template("master/bu.html", master=master, bu = b)
#   elif master == 'mm':
    # m = m3.fin()
    # return render_template("master/mm.html", master=master, mm = m)
    # return render_template("master/mm.html", master=master)
  
# @app.route("/<path:cc>")
# def cc(cc):
#   if cc == 'cement':
#     cement = sb1.fin()
#     return render_template("cc/cement.html", cc=cc, cement = cement)
#   elif cc == 'food':
#     food = sb1.fin()
#     return render_template("cc/food.html", cc=cc, food = food)

@app.route("/news")
def news():
  n = news1()
  return render_template("news.html", news1 = n)

@app.route('/test1', methods=['POST','GET'])
def backtest():
    wei.picture2

@app.route("/<path:category>")
def category(category):
  if category == '水泥工業':
    return render_template("stock/cement.html", category=category)
  elif category == '食品工業':
    return render_template("stock/food.html", category=category)
  elif category == '塑膠工業':
    return render_template("stock/plastic.html", category=category)
  elif category == '橡膠工業':
    return render_template("stock/rubber.html", category=category)
  elif category == '半導體業':
    return render_template("stock/semiconductor.html", category=category)
  elif category == '電機機械':
    return render_template("stock/motor.html", category=category)
  elif category == '電腦及週邊設備業':
    return render_template("stock/computer.html", category=category)
  elif category == '電器電纜':
    return render_template("stock/glance.html", category=category)
  elif category == '電子零組件業':
    return render_template("stock/electronic_component.html", category=category)
  elif category == '電子通路業':
    return render_template("stock/e_channel.html", category=category)
  elif category == '其他電子業':
    return render_template("stock/other_e.html", category=category)
  elif category == '資訊服務業':
    return render_template("stock/info_service.html", category=category)
  elif category == '光電業':
    return render_template("stock/optoelectronics.html", category=category)
  elif category == '油電燃氣業':
    return render_template("stock/gas.html", category=category)
  elif category == '鋼鐵工業':
    return render_template("stock/steel.html", category=category)
  elif category == '建材營造業':
    return render_template("stock/building.html", category=category)
  elif category == '化學工業':
    return render_template("stock/chemical.html", category=category)
  elif category == '汽車工業':
    return render_template("stock/car.html", category=category)
  elif category == '航運業':
    return render_template("stock/shipping.html", category=category)
  elif category == '生技醫療業':
    return render_template("stock/bio_medic.html", category=category)
  elif category == '造紙工業':
    return render_template("stock/paper.html", category=category)
  elif category == '玻璃陶瓷':
    return render_template("stock/glass.html", category=category)
  elif category == '紡織纖維':
    return render_template("stock/textile.html", category=category)
  elif category == '貿易百貨業':
    return render_template("stock/trade.html", category=category)
  elif category == '金融保險業':
    return render_template("stock/insurance.html", category=category)
  elif category == '觀光事業':
    return render_template("stock/tourism.html", category=category)
  elif category == '通信網路業':
    return render_template("stock/communication.html", category=category)
  else:
    return render_template("stock/other.html", category=category)

@app.route('/stock/<int:id>', methods=['POST','GET'])
def stock(id):
    s = s_name(id)
    f = finance(id)
    f1 = finance2(id)
    f2 = finance3(id)
    # b = bargain(id)
    return render_template('test2.html', id=id,s_name=s, finance = f, finance2 = f1, finance3 = f2)

@app.route('/test/<int:id>', methods=['POST','GET'])
def income(id):
    s = s_name(id)
    page = request.args.get('page', 1, type=int)
    bargain = Bargain.query.filter(id==Bargain.id).paginate(per_page=10, page=page, error_out=True)
    i1=I1.query.filter(I1.id==id).order_by(I1.Date.desc()).limit(1)
    i2=I2.query.filter(I2.id==id).order_by(I2.q.desc()).limit(1)
    i3=I3.query.filter(I3.id==id).order_by(I3.quarter.desc()).limit(1)
    i4=Income.query.filter(Income.id==id).order_by(Income.quarter.desc()).limit(1)
    i5=Finance.query.filter(Finance.id==id).order_by(Finance.quarter.desc()).limit(1)
    income=Income.query.filter(id==Income.id).paginate(per_page=10, page=page, error_out=True)
    balance=Balance.query.filter(id==Balance.id).paginate(per_page=10, page=page, error_out=True)
    finance=Finance.query.filter(id==Finance.id).paginate(per_page=10, page=page, error_out=True)

    return render_template('test.html',i2=i2,i1=i1,i3=i3,i4=i4,i5=i5,s_name=s,id=id,income=income,balance=balance,finance=finance,page_num=page,bargain=bargain)
@app.route('/info/<int:id>', methods=['POST','GET'])
def info(id):
    s = s_name(id)
    i1=I1.query.filter(I1.id==id).order_by(I1.Date.desc()).limit(8)
    i2=I2.query.filter(I2.id==id).order_by(I2.q.desc()).limit(8)
    i3=I3.query.filter(I3.id==id).order_by(I3.quarter.desc()).limit(8)
    i4=Income.query.filter(Income.id==id).order_by(Income.quarter.desc()).limit(8)
    i5=Finance.query.filter(Finance.id==id).order_by(Finance.quarter.desc()).limit(8)
  
    
    return render_template('info.html',s_name=s,id=id,i1=i1,i2=i2,i3=i3,i4=i4,i5=i5)
@app.route('/pic', methods=['GET', 'POST'])
def pic(): 
    ticker = "2330.TW"
    df = yf.download(ticker,"2021-01-01")
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
    
    # 1st row
    fig = go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close']
                                # showlegend=False
                                )
    
    fig1=go.Scatter(x=data.index, 
                                    y=data['MA5'], 
                                    opacity=0.7, 
                                    
                                    line=dict(color='#2894FF', width=2), 
                                    name='5日均線')
    fig2=go.Scatter(x=data.index, 
                                    y=data['MA10'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='10日均線')
    # graphs = [
    #     dict(
    #         data=[
    #             fig
    #         ],
    #         layout=dict(
    #             width='100%',
    #             height='100%'
    #         )
    #     )
    # ]
    color1 = '#00bfff'
    color2 = '#ff4000'
    data = [fig,fig1, fig2]
    layout = go.Layout(
      
            title= 'Stock ',
            titlefont=dict(
            family='Courier New, monospace',
            size=15,
            
            
            color='#7f7f7f'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            yaxis=dict(
             dtick=800,
               
              
                title='MA5',
                titlefont=dict(
                    color=color1
                ),
                tickfont=dict(
                    color=color1,
                
                    
                )
            ),
            yaxis2=dict(
                title='MA10',
                overlaying='y',
                side='right',
                titlefont=dict(
                    color=color2
                ),
                tickfont=dict(
                    color=color2
                
                )

            )

        )
   
    
    
    fig99 = go.Figure(data,layout=dict(width=500,height=500))

    graphJSON = json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('p.html', graphJSON=graphJSON)
# 接收 LINE 的資訊 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#選股（推薦）
def select_stock():
    db = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = db.cursor()
    sql = "select id from recom where buy <= 5 order by buy asc"
      
    rec = []
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            rec.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return rec
  
#加權指數的Flex
def makeFlex1(text, text1, text2, text3):
  contents={
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": text,
              "weight": "bold",
              "color": "#1DB446",
              "size": "sm"
            },
            {
              "type": "text",
              "text": text1,
              "weight": "bold",
              "size": "xxl",
              "margin": "md"
            },
            {
              "type": "box",
              "layout": "vertical",
              "margin": "xxl",
              "spacing": "sm",
              "contents": [
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "text",
                      "text": "漲跌幅",
                      "size": "sm",
                      "color": "#555555",
                      "flex": 0
                    },
                    {
                      "type": "text",
                      "text": text2,
                      "size": "sm",
                      "color": "#111111",
                      "align": "end"
                    }
                  ]
                }
              ]
            },
            {
              "type": "separator",
              "margin": "xxl"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "margin": "md",
              "contents": [
                {
                  "type": "text",
                  "text": "日期",
                  "size": "xs",
                  "color": "#aaaaaa",
                  "flex": 0
                },
                {
                  "type": "text",
                  "text": text3,
                  "color": "#aaaaaa",
                  "size": "xs",
                  "align": "end"
                }
              ]
            }
          ]
        }}
  return contents

#新聞Flex
def makeFlex2(tit, url, tit2, url2):
  contents ={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": "https://cimg.cnyes.cool/prod/news/4819236/s/64576cce3cb5f30fdac940267499a080.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": tit,
            "wrap": True,
            "weight": "bold",
            "size": "xl"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "more",
              "uri": url
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": "https://cimg.cnyes.cool/prod/news/4819082/s/934581a8b0ee29d606284d35bd31840f.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": tit2,
            "wrap": True,
            "weight": "bold",
            "size": "xl"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "more",
              "uri": url2
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "uri",
              "label": "See more",
              "uri": "https://liff.line.me/1656823480-87mjWdb2"
            }
          }
        ]
      }
    }
  ]}
  return contents

#公司Flex
def makeFlex3(num, date, date2, date3, Q, text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14, text15, text16, text17, text18, text19, text20, text21, text22):
  contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": num,
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": "，現價",
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": text1,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text2,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text3,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text4,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text5,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": num,
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": "，股價",
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text6,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "開盤",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text7,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "最高",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text8,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "最低",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text9,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text10,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": num,
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": "，財務",
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "月營收",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text11,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "每股盈餘",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text12,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "每股淨值",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text13,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業毛利率",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text14,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "稅前淨利率",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text15,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": Q,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": num,
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": "，籌碼(當日)",
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": "籌碼",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "外資",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text16,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "投信",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text17,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "自營商",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text18,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "三大法人",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text19,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date2,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
        {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": num,
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": "，行事曆",
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": "行事曆",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "除權除息日期",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text20,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "股東常會",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text21,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "現金股利發放日",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text22,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date3,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "uri",
              "label": "See more",
              "uri": "https://liff.line.me/1656823480-9kMmlJaG"
            }
          }
        ]
      }
    }
  ]}
  return contents


  contents = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "綁定註冊與登入",
        "weight": "bold",
        "size": "xl"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "color": "#1DB446",
        "action": {
          "type": "postback",
          "label": "綁定",
          "data": "link"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
    }}
  return contents

def makeFlex4(s1,s2,s3,s4,s5,p1,p2,p3,p4,p5,text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,text13,text14,text15,text16,text17,text18,text19,text20,date):
  contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "(1)",
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": s1,
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": p1,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text1,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text2,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text3,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text4,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "(2)",
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": s2,
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": p2,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text5,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text6,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text7,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text8,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "(3)",
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": s3,
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": p3,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text9,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text10,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text11,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text12,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "(4)",
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": s4,
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": p4,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text13,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text14,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text15,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text16,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "(5)",
                "weight": "bold",
                "color": "#1DB446",
                "flex": 0
              },
              {
                "type": "text",
                "text": s5,
                "weight": "bold",
                "color": "#1DB446"
              }
            ]
          },
          {
            "type": "text",
            "text": p5,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "漲跌幅",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text17,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": text18,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "成交量",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text19,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "本益比(同業平均)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": text20,
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "日期",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": date,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "uri",
              "label": "See more",
              "uri": "https://liff.line.me/1656823480-9kMmlJaG"
            }
          }
        ]
      }
    }
  ]}
  return contents

# 主動傳訊息
# def job():
#     line_bot_api.broadcast(TextSendMessage(text="早安～"+chr(0x1000A9)+ "\n" +"現在是早上的9點整，"+ "\n" +"已經開盤囉～"+chr(0x100071)+ "\n" +"趕緊前往關注最新資訊，"+ "\n" +"掌握每一刻的重要時機！"+chr(0x1000A4)))

# sched = BackgroundScheduler()
# sched.add_job(job, 'cron', day_of_week='mon-fri', hour=9)
# sched.start()

@handler.add(PostbackEvent)
def handle_postback(event):
  if event.postback.data == "link":
    user_id = event.source.user_id
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="http://stockbottttt.herokuapp.com/news?linkToken="+user_id)
        )

# 以下為 各種回覆訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

#"公司代號"+新聞
    if "，新聞" in msg:
        new = msg.split('，')
        id1 = new[0]

        url = "https://tw.stock.yahoo.com/quote/" + id1 + "/news"
        re = requests.get(url)

        soup = BeautifulSoup(re.text, "html.parser")
        data = soup.find_all("a", {
            "class": "Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled"})
        con = []

        for index, d in enumerate(data):
            if index < 2:
                title = d.text
                href = d.get("href")
                con.append(title)
                con.append(href)
            else:
                break

        content = makeFlex2(con[0], con[1], con[2], con[3])
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label=id1+"，股價", text=id1+"，股價")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330，新聞", text=id1+"2330，新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ])
                    
            ))

#2個最新新聞
    elif "股市新聞" in msg:
        base = "https://news.cnyes.com"
        url = "https://news.cnyes.com/news/cat/tw_quo"
        re = requests.get(url)

        con = []
        soup = BeautifulSoup(re.text, "html.parser")
        data = soup.find_all("a", {"class": "_1Zdp"})
        
        for index, d in enumerate(data):
            if index < 2:
              # pic = d.find_all("img", {"src": re.compile('.*?\.jpg')})
              title = d.text
              href = base + d.get("href")
              con.append(title)
              con.append(href)
            else:
                break

        content = makeFlex2(con[0], con[1], con[2], con[3])
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330，股價", text="2330，股價")),
                                    QuickReplyButton(action=MessageAction(label="2330，新聞", text="2330，新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ])
                    
            ))

#推薦股票
    elif "推薦" in msg:
        lst = select_stock()
        conlst = []
        for i in range(len(lst)):
          id1 = lst[i]
          url = "https://tw.stock.yahoo.com/quote/" + id1
          re = requests.get(url)
          soup = BeautifulSoup(re.text, "html.parser")
          data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
          data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
          result = [span.get_text() for span in data1]
          if len(result) == 0:
            data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"})
            data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c)"})
            data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c)"})
            result = [span.get_text() for span in data1]
            if len(result) == 0:
              data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
              data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
              data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)"})
              result = [span.get_text() for span in data1]
            else:
              result = result
          else:
            result = result
          nowprice = result[0]
          up_down = ''
          increase = ''
          for i in data2:
              up_down = i.text
          for i in data3:
              increase = i.text
          trend = "{} {}".format(up_down, increase)
          data4 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
          result4 = [span.get_text() for span in data4]
          num4 = result4[0]
          data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-down)"})
          result7 = [span.get_text() for span in data7]
          if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-up)"})
            result7 = [span.get_text() for span in data7]
            if len(result7) == 0:
              data7 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
              result7 = [span.get_text() for span in data7]
            else:
              result7 = result7
          else:
            result7 = result7
          text3 = result7[0]
          data5 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
          result5 = [span.get_text() for span in data5]
          text4 = result5[0]
          text5 = result5[1]
          
          conlst.append(id1)
          conlst.append(nowprice)
          conlst.append(trend)
          conlst.append(text3)
          conlst.append(text4)
          conlst.append(text5)
          conlst.append(num4)
        s1 = conlst[0]
        s2 = conlst[7]
        s3 = conlst[14]
        s4 = conlst[21]
        s5 = conlst[28]
        p1 = conlst[1]
        p2 = conlst[8]
        p3 = conlst[15]
        p4 = conlst[22]
        p5 = conlst[29]
        text1 = conlst[2]
        text5 = conlst[9]
        text9 = conlst[16]
        text13 = conlst[23]
        text17 = conlst[30]
        text2 = conlst[3]
        text6 = conlst[10]
        text10 = conlst[17]
        text14 = conlst[24]
        text18 = conlst[31]
        text3 = conlst[4]
        text7 = conlst[11]
        text11 = conlst[18]
        text15 = conlst[25]
        text19 = conlst[32]
        text4 = conlst[5]
        text8 = conlst[12]
        text12 = conlst[19]
        text16 = conlst[26]
        text20 = conlst[33]
        date = conlst[6]
        
        content = makeFlex4(s1,s2,s3,s4,s5,p1,p2,p3,p4,p5,text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,text13,text14,text15,text16,text17,text18,text19,text20,date)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330，股價", text="2330，股價")),
                                    QuickReplyButton(action=MessageAction(label="2330，新聞", text="2330，新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ]))
        )

#回傳公司資訊
    elif "，股價" in msg:
        new = msg.split('，')
        id1 = new[0]
        url = "https://tw.stock.yahoo.com/quote/" + id1
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
        data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
        result = [span.get_text() for span in data1]
        if len(result) == 0:
          data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"})
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c)"})
          data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c)"})
          result = [span.get_text() for span in data1]
          if len(result) == 0:
            data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
            data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
            data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)"})
            result = [span.get_text() for span in data1]
          else:
            result = result
        else:
          result = result
        nowprice = result[0]
        up_down = ''
        increase = ''
        for i in data2:
            up_down = i.text
        for i in data3:
            increase = i.text
        trend = "{} {}".format(up_down, increase)
        data4 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
        result4 = [span.get_text() for span in data4]
        num4 = result4[0]

        data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-down)"})
        result7 = [span.get_text() for span in data7]
        if len(result7) == 0:
          data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-up)"})
          result7 = [span.get_text() for span in data7]
          if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px)"})
            result7 = [span.get_text() for span in data7]
          else:
            result7 = result7
        else:
          result7 = result7
        text3 = result7[0]

        data5 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
        result5 = [span.get_text() for span in data5]
        text4 = result5[0]
        text5 = result5[1]

        data9 = soup.find_all("li", {"class": "price-detail-item H(32px) Mx(16px) D(f) Jc(sb) Ai(c) Bxz(bb) Px(0px) Py(4px) Bdbs(s) Bdbc($bd-primary-divider) Bdbw(1px)"})
        result9 = [li.get_text() for li in data9]
        text6 = result9[0][2:]
        text7 = result9[1][2:]
        text8 = result9[2][2:]
        text9 = result9[3][2:]
        text10 = result9[7][3:]

        url2 = "https://tw.stock.yahoo.com/quote/"+id1+"/revenue"
        re2 = requests.get(url2)
        soup2 = BeautifulSoup(re2.text, "html.parser")
        data10 = soup2.find_all("li", {"class": "Jc(c) D(ib) Miw(100px) Fxg(1) Fxs(0) Fxb(100px) Ta(end) Mend(0)"})
        result10 = [li.get_text() for li in data10]
        text11 = result10[4]

        url3 = "https://tw.stock.yahoo.com/quote/" + id1 +"/eps"
        re3 = requests.get(url3)
        soup3 = BeautifulSoup(re3.text, "html.parser")
        data12 = soup3.find_all("div", {"class": "Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc"})
        result12 = [div.get_text() for div in data12]
        text12 = result12[3]
        data11 = soup3.find_all("div", {"class": "W(112px) Ta(start)"})
        result11 = [div.get_text() for div in data11]
        Q = result11[1] 

        url4 = "https://tw.stock.yahoo.com/quote/"+id1+"/institutional-trading"
        re4 = requests.get(url4)
        soup4 = BeautifulSoup(re4.text, "html.parser")
        data13 = soup4.find_all("div", {"class": "Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc"})
        result13 = [div.get_text() for div in data13]
        text16 = result13[6]
        text17 = result13[10]
        text18 = result13[14]
        text19 = result13[18]
        data131 = soup4.find_all("time", {"class": "Fz(14px) C(#5b636a)"})
        result131 = [time.get_text() for time in data131]
        date2 = result131[1][5:]

        url5 = "https://tw.stock.yahoo.com/quote/"+id1+"/profile"
        re5 = requests.get(url5)
        soup5 = BeautifulSoup(re5.text, "html.parser")
        data14 = soup5.find_all("div", {"class": "Py(8px) Pstart(12px) Bxz(bb)"})
        result14 = [div.get_text() for div in data14]
        text13 = result14[32]
        text14 = result14[27]
        text15 = result14[31]
        text20 = result14[44]
        text21 = result14[41]
        text22 = result14[43]
        data141 = soup5.find_all("span", {"class": "Fz(14px) C(#5b636a)"})
        result141 = [span.get_text() for span in data141]
        date3 = result141[0][5:]

        content = makeFlex3(id1, num4, date2, date3, Q, nowprice, trend, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14, text15, text16, text17, text18, text19, text20, text21, text22)
        # content = makeFlex1(msg, nowprice, trend, num4)
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label=id1+"，新聞", text=id1+"，新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ])
                    ))

#加權指數 
    elif "加權指數" in msg:
        url = "https://tw.stock.yahoo.com/quote/%5ETWII"
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")

        
        data = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
        result = [span.get_text() for span in data]
        if len(result) == 0:
          data = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
          result = [span.get_text() for span in data]
        else:
          result = result
        num = result[0]

        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
        result2 = [span.get_text() for span in data2]
        if len(result2) == 0:
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
          result2 = [span.get_text() for span in data2]
        else:
          result2 = result2
        num2 = result2[0]

        data3 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
        result3 = [span.get_text() for span in data3]
        num3 = result3[0]

        content = makeFlex1(msg, num, num2, num3)
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330，股價", text="2330，股價")),
                                    QuickReplyButton(action=MessageAction(label="2330，新聞", text="2330，新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ])
                    ))


#提示訊息
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="哈囉～"+ chr(0x10008D) +"\n" +"歡迎使用StockBot！"+ "\n" +"我們將與您分享台灣股票的相關情報與資訊！"+chr(0x10002D) +"\n" +"您可以在聊天室中，輸入查詢"+ "\n" +"1. ‘公司代號’，股價，查閱個公司資訊"+ "\n" +"2. 加權指數"+ "\n" +"3. 股市新聞"+ "\n" +"4. ‘公司代號’，新聞"+ "\n" +"5. 推薦（推薦股票）"+ "\n" + "\n" +"此外，每天將有開盤通知"+chr(0x1000A4)+"，訊息接收更即時！"+ "\n" +chr(0x100077)+"貼心提醒："+ "\n" +"如果不希望提示音干擾，您可在聊天室設定選單中，將「提醒」功能關掉喔！",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330，股價", text="2330，股價")),
                                    QuickReplyButton(action=MessageAction(label="2330，新聞", text="2330，新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308，股價", text="2308，股價")),
                                    QuickReplyButton(action=MessageAction(label="2308，新聞", text="2308，新聞"))
                                ])
        ))
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#app.run()