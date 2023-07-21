import pymysql

#5年毛利率
def f1():
    lst1=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句

    sql = "select id from financial_ratio where F2 != '-' and LEFT(quarter,4) in ('2021','2020','2019','2018','2017') group by id HAVING min(F2)>10"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst1.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst1

#5年EPS
def f2():
    lst2=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "select id from (select id,sum(F7) as sf7 from financial_ratio where LEFT(quarter,4) in ('2021','2020','2019','2018','2017') group by id, LEFT(quarter,4)) as T group by id HAVING min(sf7)>1"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst2.append(a)
    except:
        print("Error: unable to fetch data")
    # 關閉資料庫連線
    db.close()
    return lst2

#近12個月每股營收大於1.5元
def f3():
    lst3=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句

    sql = "select T.id from (select id,sum(income) as sin from income_statement where quarter in ('2021Q3','2021Q2','2021Q1','2020Q4') group by id) as T, stock_year where (T.sin/stock_year.capital)>1.5 and T.id = stock_year.id group by id"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst3.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst3

#股價淨值比小於1.5
def f4():
    lst4=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT financial_ratio.id FROM financial_ratio, stock_daily WHERE financial_ratio.quarter = '2021Q3' and stock_daily.date = '2021-12-30' and round(stock_daily.Close/financial_ratio.F8, 2)<1.5 and financial_ratio.id = stock_daily.id group by id"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst4.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst4

#過濾股價5元以下,五日均量在500張以下的個股
def f5():
    lst5=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "select T.id from (select id,(sum(Volume)/5000) as sv from stock_daily where Date in ('2021-12-30','2021-12-29','2021-12-28','2021-12-27','2021-12-26') group by id) as T, stock_daily where stock_daily.Date = '2021-12-30' and stock_daily.Close > 5 and T.sv > 500 and T.id = stock_daily.id group by id"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst5.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst5

#近4季股東權益報酬率大於5%
def f6():
    lst6=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "SELECT id FROM financial_ratio WHERE quarter in ('2021Q3','2021Q2','2021Q1','2020Q4') group by id HAVING sum(F9)>5"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = ''.join(i)
            lst6.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst6

def f():
    lst1 = f1()
    lst2 = f2()
    lst3 = f3()
    lst4 = f4()
    lst5 = f5()
    lst6 = f6()
    return sorted(set(lst1) & set(lst2) & set(lst3) & set(lst4) & set(lst5) & set(lst6))

def fin():
    lst = f()
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst7 = []
    for i in range(len(lst)):
        # SQL 查詢語句
        sql = "SELECT * FROM stock WHERE id =" + lst[i]

        cursor.execute(sql)
        lst7.extend(cursor.fetchall())

    # 關閉資料庫連線
    db.close()
    return lst7