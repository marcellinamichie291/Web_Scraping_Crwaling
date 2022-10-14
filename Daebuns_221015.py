import pymysql
import FinanceDataReader as fdr

## Mysql 연동부
conn = pymysql.connect(host='localhost', user='root', password='0000', db='DaeBuns', charset='utf8mb4')
cursor = conn.cursor()
cursor.execute('drop table IF EXISTS stocks')
sql = """create table stocks (
    date varchar(10) NOT NULL,
    sno char(6) NOT NULL,
    open INT,
    high INT,
    low INT,
    close INT,
    primary key(date))"""

cursor.execute(sql)

start_date = '2013-10-14'
end_date = '2022-10-14'
symbol = '005930'

df = fdr.DataReader(symbol = symbol, start=start_date, end=end_date)

# 데이터 삽입부
for i in range(len(df)):
    sno = str(symbol)
    date = str(df.iloc[i].name.date())
    open = str(df.iloc[i][0])
    high = str(df.iloc[i][1])
    low = str(df.iloc[i][2])
    close = str(df.iloc[i][3])

    # 각 변수는 꼭 str형태로 만들어줘서 python + 연산이 가능하도록!! ( 안하면 충돌 )
    # 어차피 table의 자료형은 INT로 저장되어있고 + ' ' 로 감싸주지 않으면 숫자만 잘 넘어감(string 형태가 넘어가는 것이 아님) 
    sql = "insert into stocks values('" + date + "','" + sno + "'," + open + "," + high + "," + low + "," + close + ")"
    
    try:
        cursor.execute(sql)
        conn.commit() # cursor.commit() 아님
    except pymysql.err.InternalError as e:
	    code, msg = e.args

# 데이터 확인부
cursor.execute("select * from stocks")
rows = cursor.fetchall()
for cur_row in rows:
    sno = cur_row[0]
    date = cur_row[1]
    open = cur_row[2]
    high = cur_row[3]
    low = cur_row[4]
    close = cur_row[5]
    print("%6s %10s %7d %7d %7d %7d " %(sno, date, open,high,low,close))

