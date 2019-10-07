import pyodbc
import csv

def GetData(filename):
    data = []
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile)
        count = 0
        for row in rows:
            data.append(row)
            count += 1
    print('共', count, '筆資料')
    return data


def InsertScore(data, gas):
    #連線字串
    connStr = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=localhost;DATABASE=air;Trusted_Connection=yes'
    # 連線
    conn = pyodbc.connect(connStr)
    #成功後，後面的程式都使用conn 這個物件代表資料庫連線
    # 建立cursor，這是資料查詢用的機制
    cursor = conn.cursor()
    count = 0
    for row in data:
        #print(row)
        
        if count != 0:
            sql = 'insert into ' + gas + ' values('
            sql += str(count) + ', '
            sql += row[0][0:3]
            if row[0][5] == '月':
                sql += '0' + row[0][4:5] + ', \''
            else:
                sql += row[0][4:6] + ', \''
            sql += row[1] + '\', \''
            sql += row[2] + '\', \''
            sql += row[3] + '\', '
            if gas == '非甲烷碳氫化合物':
                sql += row[5] + ')'
            else:
                sql += row[6] + ')'
            # 將SQL 命令送去執行，查詢結果放入cursor內
            cursor.execute(sql)
        cursor.commit()
        count += 1

    conn.close()
    print('一共轉入', count, '筆資料')

def main():
    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-一氧化碳.csv')
    InsertScore(data, '一氧化碳')
    
    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-二氧化硫.csv')
    InsertScore(data, '二氧化硫')

    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-二氧化氮.csv')
    InsertScore(data, '二氧化氮')

    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-非甲烷碳氫化合物.csv')
    InsertScore(data, '非甲烷碳氫化合物')

    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-臭氧.csv')
    InsertScore(data, '臭氧')

    data = GetData('臺北市環境空氣品質監測結果/臺北市環境空氣品質監測結果-懸浮微粒.csv')
    InsertScore(data, '懸浮微粒')

try:
    main()
except KeyboardInterrupt:
    print('關閉程式')
