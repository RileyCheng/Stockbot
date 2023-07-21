import pymysql

def f():
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
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