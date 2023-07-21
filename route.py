from crypt import methods
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask,render_template,url_for
import pandas as pd
from soupsieve import select
from sqlalchemy import create_engine
import numpy as np
import talib
import os
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas as pd
import json
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net:3306/heroku_da386d83e593c1d"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net/heroku_da386d83e593c1d"
db = SQLAlchemy(app)
conn = pymysql.connect(
    host='us-cdbr-east-05.cleardb.net',
    user='be59caf2e81229',
    password='75242529',
    db='heroku_da386d83e593c1d',
    charset='utf8'
)
@app.route("/picture",methods=['POST','GET'])
def picture():
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('picture.html',graph1JSON=graph1JSON)
