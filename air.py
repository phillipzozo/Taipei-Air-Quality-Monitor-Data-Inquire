import math
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


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
    

#圖表
def plotData(plt, data):
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    plt.plot(x, y, '-o')

def printGraph():
    data_1 = [
      (1,2), (3,4), (5,2), (7,5), (9,8)
    ]
    data_2 = [
      (1,1), (3,6), (3,9), (7,9), (9,3)
    ]
    plotData(plt, data_1)
    plotData(plt, data_2)
    plt.show()

    
def main():
    #data = GetData('臺北市環境空氣品質監測結果.csv')
    printGraph()

    
main()
