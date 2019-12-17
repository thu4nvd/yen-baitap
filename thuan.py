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


def fill_one_not_3(series):
    zeros = (True, True, True)
    runs = [tuple(x == 1 for x in r)
            for r in zip(*(series.shift(i)
                           for i in (-2, -1, 0, 1, 2)))]
    need_fill = [(r[0:3] != zeros and r[1:4] != zeros and r[2:5] != zeros)
                 for r in runs]
    retval = series.copy()
    retval[need_fill] = 1
    return retval


def count_heat(series):
    count = 0
    for r in zip(series, series.shift(-1))
        if r = (0, 1):
            count += 1 
    return count


if __name__ == '__main__':
    filelist = glob.glob('./out/*.txt')
    for f in filelist:
        station = f[f.rfind('/')+1:f.rfind('_')] #extract name of station from file name
        df = ReadCSVFile(f)
        threshold = df['TEMP'].quantile(0.9)    #calculate percentile of station
        df.loc[(df.temp >= threshold),'tag'] = 1
        df.loc[(df.temp < threshold),'tag'] = 0
        df['tag'] = fill_one_not_3(df['tag'])   #if value tag = 1 but not 3 consecutive value -> assign to 0
        df.groupby('YEAR').count_heat()
        
