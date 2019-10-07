import math
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


#取得檔案
def GetData(filename):
    # 開啟 CSV 檔案
    with open(filename, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)

        count = 0
        temp_data = []
        # 以迴圈輸出每一列
        for row in rows:
            temp_data.append(row)
            count += 1
            #print(row)
            #for item in row:
                #print(item, end=' ')
            #print()
        
        print('共', count, '筆資料')
        return temp_data


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def plot(x, y):
    plt.clf()
    plt.plot(x,y)
    # just plt.draw() won't do it here, strangely
    plt.gcf().canvas.draw()

# just to see the plot change
plotShift = 0
def main():
    global plotShift

    x = np.arange(0.0,3.0,0.01)
    y = np.sin(2*np.pi*x + plotShift)
    plot(x, y)
    
    plotShift += 1
    print(plotShift)

def _query():
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

    sql = 'SELECT * from ' + gas + ' as A ' #要加空白
    sql += 'WHERE A.年月 BETWEEN ' + start_year+start_month + ' and ' + end_year+end_month + ' ' # ? 可在 execute 中再套函數
    sql += 'and A.監測站 = \'' + area + '\' '
    sql += 'order by A.編號'
    print(sql)

    #data = GetData('臺北市環境空氣品質監測結果.csv')
    data_1 = [
        (1,2), (3,4), (5,2), (7,5), (9,8)
    ]
    data_2 = [
        (1,1), (3,6), (3,9), (7,9), (9,3)
    ]

    #圖表
    x = [p[0] for p in data_1]
    y = [p[1] for p in data_1]
    x2 = [p[0] for p in data_2]
    y2 = [p[1] for p in data_2]

    plt.clf()
    l1, = plt.plot(x, y, '-o')
    l2, = plt.plot(x2, y2, '-o', color='red', linewidth=1.0)
    plt.legend(handles=[l1,l2,], labels=['aaa','bbb'], loc='best')
    
    #set x limits
    plt.xlim((0, 13))
    plt.ylim((0, 20))
    plt.xlabel('year / month')
    plt.ylabel('ppm')
    
    # set line syles
    #l1, = plt.plot(x, y, label='linear line')
    #l2, = plt.plot(x2, y2, color='red', linewidth=1.0, linestyle='--', label='square line')
    #plt.legend(handles=[l1,l2,],labels=['aaa','bbb'],loc='best')
    
    plt.gcf().canvas.draw()
    

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

    #search area
    frm_form = tk.Frame(root)
    frm_form.pack(side=tk.LEFT, expand=1)
    
    frm_search = tk.Frame(frm_form)
    frm_search.pack(side=tk.TOP, padx=10, pady=100, expand=1)
    
    label_title = ttk.Label(frm_search, text="查詢條件", font=("微軟正黑體", 14))
    label_title.pack(side=tk.TOP, fill=tk.X, expand=1)

        #date area
            #start time
    frm_date_from = tk.Frame(frm_search)
    frm_date_from.pack(side=tk.TOP, pady=4, expand=1)
    label_date_from = ttk.Label(frm_date_from, text="起始時間：", font=("微軟正黑體", 10))
    label_date_from.pack(side=tk.LEFT, fill=tk.X, expand=1)
            #choice
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

            #end time
    frm_date_to = tk.Frame(frm_search)
    frm_date_to.pack(side=tk.TOP, pady=4, expand=1)
    label_date_to = ttk.Label(frm_date_to, text="結束時間：", font=("微軟正黑體", 10))
    label_date_to.pack(side=tk.LEFT, fill=tk.X, expand=1)
            #choice
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

        #gas choice
    frm_gas = tk.Frame(frm_search)
    frm_gas.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    label_gas = ttk.Label(frm_gas, text="　　氣體：", font=("微軟正黑體", 10))
    label_gas.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    gas = sorted(set(i for i in data[2]))
    combobox_gas = ttk.Combobox(frm_gas, width=15, value=gas, state='readonly')
    combobox_gas.set(gas[0])
    combobox_gas.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
        #area choice
    frm_area = tk.Frame(frm_search)
    frm_area.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    label_area = ttk.Label(frm_area, text="　　地區：", font=("微軟正黑體", 10))
    label_area.pack(side=tk.LEFT, fill=tk.X, expand=1)
    
    area = sorted(set(i for i in data[3]))
    combobox_area = ttk.Combobox(frm_area, width=10, value=area, state='readonly')
    combobox_area.set(area[0])
    combobox_area.pack(side=tk.LEFT, fill=tk.X, expand=1)

        #submit button
    button_query = ttk.Button(master=frm_search, text="查詢", command = _query)
    button_query.pack(side=tk.TOP, fill=tk.X, expand=1)

    #quit button
    frm_quit = tk.Frame(frm_form)
    frm_quit.pack(side=tk.TOP, anchor="w", pady=4, expand=1)
    button_quit = ttk.Button(master=frm_quit, text="離開", command = _quit)
    button_quit.pack(side=tk.BOTTOM, fill=tk.X, padx=10, expand=1)

    
    #pic area
    frm_pic = tk.Frame(root)
    frm_pic.pack(side=tk.LEFT, fill=tk.Y, expand=1)
    
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


