import pymysql
import yfinance as yf

def f1():
    grow_lst=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F19 FROM financial_ratio where quarter='2021Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        grow = cursor.fetchall()
        for i in grow:
            grow_lst.append(i)
    except:
        print("Error: unable to fetch data")
    db.close()
    return grow_lst

def f2():
    grow_lst2=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql2=  "SELECT id,F19 FROM financial_ratio where quarter='2020Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql2)
        # 獲取所有記錄列表
        grow2 = cursor.fetchall()
        for i in grow2:
            grow_lst2.append(i)
    except:
        print("Error: unable to fetch data")
    db.close()
    return grow_lst2

def f3():
    grow_lst = f1()
    grow_lst2 = f2()
    pa=[]
    for i in range(len(grow_lst)):
        
            if grow_lst[i][1]== '-' or grow_lst2[i][1]== '-':
                continue
            else:
                c=(float(grow_lst[i][1])+float(grow_lst2[i][1]))/2
                re=grow_lst[i][0],format(c,'.2f')
                if float(re[1])>25:
                    pa.append(re[0])
    return pa

#稅前成長率
def f4():
    pa = f3()
    ebs_lst=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F21 FROM financial_ratio where quarter='2021Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs = cursor.fetchall()
        for i in ebs:
            ebs_lst.append(i)
    except:
        print("Error: unable to fetch data")
    co=[]
    for i in range(len(ebs_lst)):
        if str(ebs_lst[i][0]) in str(pa):
            co.append(ebs_lst[i][0])
    db.close()
    return co

def f5():
    pa = f3()
    ebs_lst2=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2020Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs2 = cursor.fetchall()
        for i in ebs2:
            ebs_lst2.append(i)
    except:
        print("Error: unable to fetch data")
    co2=[]
    for i in range(len(ebs_lst2)):
        if str(ebs_lst2[i][0]) in str(pa):
            co2.append(ebs_lst2[i][0])
    db.close()
    return co2
      
def f6():
    pa = f3()
    ebs_lst3=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2019Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs3 = cursor.fetchall()
        for i in ebs3:
            ebs_lst3.append(i)
    except:
        print("Error: unable to fetch data")

    co3=[]
    for i in range(len(ebs_lst3)):
        if str(ebs_lst3[i][0]) in str(pa):
            co3.append(ebs_lst3[i][0])    
    db.close()  
    return co3

def f7():
    pa = f3()
    ebs_lst4=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2018Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs4 = cursor.fetchall()
        for i in ebs4:
            ebs_lst4.append(i)
    except:
        print("Error: unable to fetch data")

    co4=[]
    for i in range(len(ebs_lst4)):
        if str(ebs_lst4[i][0]) in str(pa):
            co4.append(ebs_lst4[i][0])
    db.close()
    return co4

def f8():
    pa = f3()
    ebs_lst5=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2017Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs5 = cursor.fetchall()
        for i in ebs5:
            ebs_lst5.append(i)
    except:
        print("Error: unable to fetch data")
        
    co5=[]
    for i in range(len(ebs_lst5)):
        if str(ebs_lst5[i][0]) in str(pa):
            co5.append(ebs_lst5[i][0])
    db.close()
    return co5

def f9():
    d=[f4(),f5(),f6(),f7(),f8()]
    result=set(d[0]).intersection(*d[1:])
    result=sorted(list(result))   
    return result

def f10():
    result = f9()
    ebs_lst5a=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2017Q3'"
    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs5a = cursor.fetchall()
        for i in ebs5a:
            ebs_lst5a.append(i)
    except:
        print("Error: unable to fetch data")
        
    co5a=[]
    for i in range(len(ebs_lst5a)):
        if str(ebs_lst5a[i][0]) in str(result):
            co5a.append(ebs_lst5a[i])
    co5a=sorted(list(set(co5a)))     
    db.close() 
    return co5a

def f11():
    result = f9()
    ebs_lst4a=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2018Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs4a = cursor.fetchall()
        for i in ebs4a:
            ebs_lst4a.append(i)
    except:
        print("Error: unable to fetch data")

    co4a=[]
    for i in range(len(ebs_lst4a)):
        if str(ebs_lst4a[i][0]) in str(result):
            co4a.append(ebs_lst4a[i])
    co4a=sorted(list(set(co4a)))
    db.close()
    return co4a

def f12():
    result = f9()
    ebs_lst3a=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2019Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs3a = cursor.fetchall()
        for i in ebs3a:
            ebs_lst3a.append(i)
    except:
        print("Error: unable to fetch data")

    co3a=[]
    for i in range(len(ebs_lst3a)):
        if str(ebs_lst3a[i][0]) in str(result):
            co3a.append(ebs_lst3a[i])
    co3a=sorted(list(set(co3a)))
    db.close()
    return co3a

def f13():
    result = f9()
    ebs_lst2a=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F20 FROM financial_ratio where quarter='2020Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebs2a = cursor.fetchall()
        for i in ebs2a:
            ebs_lst2a.append(i) 
    except:
        print("Error: unable to fetch data")
        
    co2a=[]
    for i in range(len(ebs_lst2a)):
        if str(ebs_lst2a[i][0]) in str(result):
            co2a.append(ebs_lst2a[i])
    co2a=sorted(list(set(co2a)))
    db.close()
    return co2a

def f14():
    result = f9()
    ebs_lsta=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F21 FROM financial_ratio where quarter='2021Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        ebsa = cursor.fetchall()
        for i in ebsa:
            ebs_lsta.append(i)
    except:
        print("Error: unable to fetch data")
    coa=[]
    for i in range(len(ebs_lsta)):
        if str(ebs_lsta[i][0]) in str(result):
            coa.append(ebs_lsta[i])
    coa=sorted(list(set(coa)))
    db.close()
    return coa

#篩選近5稅前>7%
def f15():
    coa = f14()
    co2a = f13()
    co3a = f12()
    co4a = f11()
    co5a = f10()
    ave=[]
    for i in range(len(coa)):
        if coa[i][1]== '-' or co2a[i][1]== '-' or co3a[i][1]== '-' or co4a[i][1]== '-' or co5a[i][1]== '-':
            continue
        else:
            c=(float(coa[i][1])+float(co2a[i][1])+float(co3a[i][1])+float(co4a[i][1])+float(co5a[i][1]))/5
            result=coa[i][0],format(c,'.2f')
            
            if float(result[1])>7:
                ave.append(result[0])
    return ave

#近季負債比率
def f16():
    ave = f15()
    lia_lst=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,F54 FROM financial_ratio where quarter='2021Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        lia = cursor.fetchall()
        for i in lia:
            lia_lst.append(i)  
    except:
        print("Error: unable to fetch data")
        
    lia_up=[]
    for i in range(len(lia_lst)):
        if str(lia_lst[i][0]) in str(ave):
            lia_up.append(lia_lst[i])
    lia_up=sorted(list(set(lia_up)))
    
    #篩選負債
    lia=[]
    for i in range(len(lia_up)):
        if lia_up[i][1]== '-' :
            continue
        else:
            if float(lia_up[i][1]) <30:
                result=lia_up[i]
                lia.append(result[0])
    db.close()
    return lia

#本益比<20
def f17():
    lia = f16()
    pe_lst=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql =  "SELECT id,pe FROM stock_pe where q='21Q3'"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        pe = cursor.fetchall()

        for i in pe:
            pe_lst.append(i) 
    except:
        print("Error: unable to fetch data")
        
    pe_lsta=[]
    for i in range(len(pe_lst)):
        if str(pe_lst[i][0]) in str(lia):
            pe_lsta.append(pe_lst[i])
    pe_lsta=sorted(list(set(pe_lsta)))
    pe=[]
    for i in range(len(pe_lsta)):
        if pe_lsta[i][1]== None :
            continue
        else:
            if float(pe_lsta[i][1]) <20:
                result=pe_lsta[i]
                pe.append(result[0])
    db.close()
    return pe

def f18():
    #股價大於多少
    pe = f17()
    stock=[]
    for i in pe:
    
        st=yf.Ticker(str(i)+'.TW')
        st=st.history(start='2021-12-30',end='2021-12-31')
        st=st['Close']
        st=format(float(st),'.1f')
        
        if float(st)>5:
            stock.append(i)

    #成交量大於多少
    volume=[]
    for i in stock:
    
        vo=yf.Ticker(str(i)+'.TW')
        vo=vo.history(start='2021-12-24',end='2021-12-31')
        vo=vo['Volume']
        sumvo=0
        for j in vo:
            sumvo+=j
        sumvo=sumvo/5000
        if sumvo>500:
            volume.append(i)
    return volume

def fin():
    lst = f18()
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lsta = []
    for i in range(len(lst)):
        # SQL 查詢語句
        sql = "SELECT * FROM stock WHERE id =" + str(lst[i])

        cursor.execute(sql)
        lsta.extend(cursor.fetchall())

    # 關閉資料庫連線
    db.close()
    return lsta