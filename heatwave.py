import pandas as pd
import numpy as np
import matplotlib.plot as plot
import glob

#- mỗi file là dữ liệu của 1 trạm khí tượng (trong khoảng 30 năm) theo cấu trúc 
# YEAR - MONTH - DAY - VALUE (Nhiệt độ ngày )
# Yc:
# Ve bieu do tung tram
###

def ReadCSVFile(filename):
    df = pd.read_csv(filename, sep='\s+', names=['YEAR','MONTH','DATE','TEMP'])
    return df

def Ca ():
    


if __name__ == '__main__':
    filelist = glob.glob('./out/*.txt')
    for f in filelist:
        station = f[f.rfind('/')+1:f.rfind('_')]
        df = ReadCSVFile(f)
