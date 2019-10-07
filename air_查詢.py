import math
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt  #pip install matplotlib

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import pyodbc


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def _query():
    #取得各選項內容
    start_year = combobox_start_date_year.get()
    start_month = combobox_start_date_month.get()
    end_year = combobox_end_date_year.get()
    end_month = combobox_end_date_month.get()
    gas = combobox_gas.get()
    area = combobox_area.get()

    if len(start_month) < 2:
        start_month = '0' + start_month
    if len(end_month) < 2:
        end_month = '0' + end_month

    print('起始時間：' + start_year+ '年'+start_month + '月')
    print('結束時間：' + end_year+ '年'+end_month + '月')
    print('氣體：' + gas)
    print('站點：' + area)
    label_area_pic.config(text = area)
    
    #連線字串
    connStr = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=localhost;DATABASE=air;Trusted_Connection=yes'

    # 連線
    conn = pyodbc.connect(connStr)

    #成功後，後面的程式都使用conn 這個物件代表資料庫連線
    # 建立cursor，這是資料查詢用的機制
    cursor = conn.cursor()
    
    sql = 'SELECT * from ' + gas + ' as A ' #要加空白
    sql += 'WHERE A.年月 BETWEEN ' + start_year+start_month + ' and ' + end_year+end_month + ' '
    sql += 'and A.監測站 = \'' + area + '\' '
    sql += 'order by A.編號'

    # 將SQL 命令送去執行，查詢結果放入cursor內
    cursor.execute(sql)

    #將傳出來的結果取出 並逐筆處理
    rows = cursor.fetchall()
    cnt = 0
    year_month = []
    month_avg = []
    for row in rows:
        print(row.編號, row.年月, row.監測項目, row.監測站, row.監測站編號, row.月平均)
        year_month.append(str(row.年月)[0:3] + str(row.年月)[3:])
        month_avg.append(str(row.月平均))
        cnt += 1
    print('共', cnt, '筆資料')
    print()
    #將時間及濃度加入陣列 (時間, 濃度)
    data_1 = []
    for i in range(len(year_month)):
        data_1.append((year_month[i], float(month_avg[i])))
        

    # x為月份 y為濃度
    x = [p[0] for p in data_1]
    y = [p[1] for p in data_1]

    #畫線
    plt.clf()
    l1, = plt.plot(x, y, '-o')
    #l2, = plt.plot(x2, y2, color='red', linewidth=1.0, linestyle='--', label='square line')
    plt.legend(handles=[l1,], labels=[gas_eng[gas]], loc='best')
    
    #set x limits x軸最小最大值
    plt.xlim((0, year_month[len(year_month)-1]))
    #plt.ylim((month_avg[0], month_avg[len(month_avg)-1]))
    #x y 軸名稱
    plt.xlabel('year / month')
    plt.ylabel('ppm')
    
    plt.gcf().canvas.draw()

    conn.close()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

try:
    print('Press Ctrl-C to exit.')
    
    data = []
    data.append([104, 105])
    data.append([i for i in range(1, 13)])
    data.append(['一氧化碳', '二氧化硫', '二氧化氮', '非甲烷碳氫化合物', '臭氧', '懸浮微粒'])
    data.append(['中正站', '大直站', '信義站', '南港站', '內湖站', '木柵站', '承德站'])
    
    
    #creatWindow
    root = tk.Tk()
    root.title('臺北市環境空氣品質監測結果查詢')
    #root.width = 500
    #root.height = 200
    root.resizable(0,0)  #lock size

    #search area 搜尋區
    frm_form = tk.Frame(root)
    frm_form.pack(side=tk.LEFT, expand=1)
    
    frm_search = tk.Frame(frm_form)
    frm_search.pack(side=tk.TOP, padx=10, pady=100, expand=1)
    
    label_title = ttk.Label(frm_search, text="查詢條件", font=("微軟正黑體", 14))
    label_title.pack(side=tk.TOP, fill=tk.X, expand=1)

        #date area 時間選擇
            #start time 開始時間
    frm_date_from = tk.Frame(frm_search)
    frm_date_from.pack(side=tk.TOP, pady=4, expand=1)
    label_date_from = ttk.Label(frm_date_from, text="起始時間：", font=("微軟正黑體", 10))
    label_date_from.pack(side=tk.LEFT, fill=tk.X, expand=1)
            #choice 下拉式選單
    date = sorted(set(i for i in data[0]))
    month = sorted(set(i for i in data[1]))
    combobox_start_date_year = ttk.Combobox(frm_date_from, width=5, value=date, state='readonly')
    combobox_start_date_year.set(date[0])
    combobox_start_date_year.pack(side=tk.LEFT, fill=tk.X, expand=1)
    label_date_year = ttk.Label(frm_date_from, text="年", font=("微軟正黑體", 10))
    label_date_year.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    combobox_start_date_month = ttk.Combobox(frm_date_from, width=5, value=month, state='readonly')
    combobox_start_date_month.set(month[0])
    combobox_start_date_month.pack(side=tk.LEFT, fill=tk.X, expand=1)
    label_date_month = ttk.Label(frm_date_from, text="月", font=("微軟正黑體", 10))
    label_date_month.pack(side=tk.LEFT, fill=tk.X, expand=1)

            #end time 結束時間
    frm_date_to = tk.Frame(frm_search)
    frm_date_to.pack(side=tk.TOP, pady=4, expand=1)
    label_date_to = ttk.Label(frm_date_to, text="結束時間：", font=("微軟正黑體", 10))
    label_date_to.pack(side=tk.LEFT, fill=tk.X, expand=1)
            #choice 下拉式選單
    combobox_end_date_year = ttk.Combobox(frm_date_to, width=5, value=date, state='readonly')
    combobox_end_date_year.set(date[0])
    combobox_end_date_year.pack(side=tk.LEFT, fill=tk.X, expand=1)
    label_date_year = ttk.Label(frm_date_to, text="年", font=("微軟正黑體", 10))
    label_date_year.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    combobox_end_date_month = ttk.Combobox(frm_date_to, width=5, value=month, state='readonly')
    combobox_end_date_month.set(month[0])
    combobox_end_date_month.pack(side=tk.LEFT, fill=tk.X, expand=1)
    label_date_month = ttk.Label(frm_date_to, text="月", font=("微軟正黑體", 10))
    label_date_month.pack(side=tk.LEFT, fill=tk.X, expand=1)

        #gas choice 氣體選擇
    frm_gas = tk.Frame(frm_search)
    frm_gas.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    label_gas = ttk.Label(frm_gas, text="　　氣體：", font=("微軟正黑體", 10))
    label_gas.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    gas = sorted(set(i for i in data[2]))
    combobox_gas = ttk.Combobox(frm_gas, width=15, value=gas, state='readonly')
    combobox_gas.set(gas[0])
    combobox_gas.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
        #area choice 地區選擇
    frm_area = tk.Frame(frm_search)
    frm_area.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    label_area = ttk.Label(frm_area, text="　　地區：", font=("微軟正黑體", 10))
    label_area.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    area = sorted(set(i for i in data[3]))
    combobox_area = ttk.Combobox(frm_area, width=10, value=area, state='readonly')
    combobox_area.set(area[0])
    combobox_area.pack(side=tk.LEFT, fill=tk.X, expand=1)

        #submit button 查詢按鈕
    button_query = ttk.Button(master=frm_search, text="查詢", command = _query)
    button_query.pack(side=tk.TOP, fill=tk.X, expand=1)
    
        #gas table 氣體中英文表
    frm_gas_chi_eng = tk.Frame(frm_search)
    frm_gas_chi_eng.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    
    gas_eng = {'一氧化碳':'Carbon monoxide',
               '二氧化硫':'Sulfur dioxide',
               '二氧化氮':'Nitrogen dioxide',
               '非甲烷碳氫化合物':'Non-methane hydrocarbon',
               '臭氧':'ozone',
               '懸浮微粒':'Suspended particles'}

    chi_eng = ['中文','英文']
    tree = ttk.Treeview(frm_gas_chi_eng, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6'),
                            show="headings")#表格
    tree["columns"]=('中文','英文')
    tree.column('中文', width=120, anchor='e')   #表示列,不顯示
    tree.column('英文', width=120, anchor='w')
    tree.heading('中文',text='中文')  #顯示表頭
    tree.heading('英文',text='英文')
    
    for i in range(len(gas)):
        tree.insert("", i, values=(gas[i], gas_eng[gas[i]])) #插入數據
    
    tree.pack(side=tk.TOP, expand=1)

    #quit button 離開按鈕
    frm_quit = tk.Frame(frm_form)
    frm_quit.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    button_quit = ttk.Button(master=frm_quit, text="離開", command = _quit)
    button_quit.pack(side=tk.BOTTOM, fill=tk.X, padx=10, expand=1)

    
    #pic area 圖表
    frm_pic = tk.Frame(root)
    frm_pic.pack(side=tk.LEFT, fill=tk.Y, expand=1)
    
    label_area_pic = ttk.Label(frm_pic, text=combobox_area.get(), font=("微軟正黑體", 16))
    label_area_pic.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    fig = plt.figure(figsize=(5, 4), dpi=100)
    
    canvas = FigureCanvasTkAgg(fig, master=frm_pic)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frm_pic)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    canvas.mpl_connect("key_press_event", on_key_press)

    
    #show window
    root.mainloop()
    
except:
    print('Progarm is stop.')
