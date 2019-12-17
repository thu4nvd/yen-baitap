import numpy as np 
import pandas as pd 
import glob
import matplotlib.pyplot as plt 
#import geopandas as geo


def ReadInputCSVFiles(filename):
    print(filename)
    df = pd.read_csv(filename)
    return df


def ReadInputTXTFiles(filename):
    print(filename)
    df = pd.read_fwf(filename)
    col = ['YEAR', 'MONTH', 'DAY', 'DATA']
    df.columns = col
    ind = df['DATA'] == 99
    df.loc[ind,'DATA'] = -99.
        
    return df


def HeatWaveIdentification(df,col,quant): 
    hwn = dict()   #dict of heatwave number for specific station
    hwd_max = dict() #dict of heatwave duration for longest duration
    hwd_mean = dict() #dict of heatwave duration for mean of duration

    # Idenfify quantile 
    df[df[col]<= -99] = np.nan
    df = df[(df['MONTH']>3) & (df['MONTH']<10)]
    hw_thres = df[col].quantile(quant)
    hw_thres = float(hw_thres, )
    # print('thres:', hw_thres)

    # Count number of year
    years = df['YEAR'].unique()

    for yr in years:
        df2 = df[df['YEAR']==yr]
        # HEATWAVE DETECTION
        # tag rows based on the threshold
        df2['tag'] = df2[col] > hw_thres

        # first row is a True preceded by a False (first month of an event)
        fst = df2.index[df2['tag'] & ~ df2['tag'].shift(1).fillna(False)]
        
        # last row is a True followed by a False (last month of an event)
        lst = df2.index[df2['tag'] & ~ df2['tag'].shift(-1).fillna(False)]

        durations = lst - fst + 1
        durations3 = [i for i in durations if i >= 3]
        # durations = durations[durations>=3]
        # num_years = df2.iloc[-1]['YEAR'] - df2.iloc[0]['YEAR'] + 1.
        # print(yr,'--------------------')
        # print('Number of heat wave:', len(durations))
        hwn[yr] = len(durations3)
        hwd_max[yr] = 0 if not len(durations3) else max(durations3)
        hwd_mean[yr] = 0 if not len(durations3) else sum(durations3)/len(durations3)
        #print('Lon nhat', max(durations))
        # print('Number of heat wave per year:', len(durations)/num_years)
        # for i in range(len(fst)):
        #     if durations[i] >=3:
        #         print(df2.loc[fst[i]:lst[i],'DATA'].mean())

    # return fst, lst, durations, df
    return hwn, hwd_max, hwd_mean, hw_thres


if __name__ == '__main__':

    # filelist = glob.glob('T*.csv')
    filelist2 = glob.glob('Daily_TXT/*.txt')
    hw_thres = dict()
    hwn = dict()
    hwd_max = dict()
    hwd_mean = dict()
    hw_thres = dict()

    for f in filelist2:
        # Doc du lieu tu file        
        # df = ReadInputCSVFiles(f)
        df = ReadInputTXTFiles(f)
        station = f[f.rfind('/')+1:f.rfind('_')]

        # Xac dinh heat wave    
        hwn[station], hwd_max[station], hwd_mean[station], hw_thres[station]  = HeatWaveIdentification(df,'DATA',0.9)

    #ve bieu do heatwave number
    # print(hwn.keys())
    for s in hwn.keys():
        dfpl = pd.Series(hwn[s])
        # dfpl = dfpl.cumsum()
        dfpl.plot()
        plt.xlabel('Year')
        plt.ylabel('Number of Heatwave')
        plt.suptitle(s + " (threshold =" + '%.2f' % hw_thres[s] + ")")
        plt.savefig('./pics/'+s)
        plt.close('all')

    #ve bieu do heatwave duration max
    # print(hwn.keys())
    for s in hwd_max.keys():
        dfpl = pd.Series(hwd_max[s])
        # dfpl = dfpl.cumsum()
        dfpl.plot()
        plt.xlabel('Year')
        plt.ylabel('Max duration')
        plt.suptitle(s)
        plt.savefig('./pics_duration/'+s)
        plt.close('all')