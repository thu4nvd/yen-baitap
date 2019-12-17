import numpy as np 
import pandas as pd 
import glob
import matplotlib.pyplot as plt 


def ReadInputCSVFiles(filename):
    print(filename)
    df = pd.read_csv(filename)
    return df


def ReadInputTXTFiles(filename):
    print(filename)
    info = pd.read_csv(filename, nrows=0)
    sta = info.columns[0].split()
    df = pd.read_fwf(filename, skiprows=[0])
    col = ['Date', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df.columns = col

    years = df[df['Date']>1900],['Date']

    # 2. Extract year list and create date range
    date_start = str(years.iloc[0])+'-01-01'
    date_end = str(years.iloc[-1])+'-12-31'
    daterng = pd.date_range(start=date_start, end=date_end, freq='D')
    data = np.nan * np.zeros(daterng.size)
    df2 = pd.DataFrame(data, columns = [sh], index=daterng)
    
    # 3. Convert table to 1D array
    for yr in years:
        ind1 = np.where(df['Date']==yr)[0][0]
        ind2 = np.where(df2.index==str(yr)+'-01-01')[0][0]
        k = 0
        for mon in range(1,13):
            num_day_month = pd.Period(str(yr)+'-'+str(mon)).days_in_month
            for day in range(1, num_day_month+1):
                df2.iloc[ind2+k][sh] = df.iloc[ind1+day][df.columns[mon]]
                k += 1

    return sta, df


def HeatWaveIdentification(df,col,quant): 
    # Idenfify quantile 
    df = df[df['YEAR']==2014]
    hw_thres = df[col].quantile(quant)
    print('thres:', hw_thres)

    # HEATWAVE DETECTION
    # tag rows based on the threshold
    df['tag'] = df[col] > hw_thres

    # first row is a True preceded by a False (first month of an event)
    fst = df.index[df['tag'] & ~ df['tag'].shift(1).fillna(False)]
    
    # last row is a True followed by a False (last month of an event)
    lst = df.index[df['tag'] & ~ df['tag'].shift(-1).fillna(False)]

    durations = lst - fst + 1
    durations = durations[durations>=3]
    num_years = df.iloc[-1]['YEAR'] - df.iloc[0]['YEAR'] + 1.
    print('Number of heat wave:', len(durations))
    print('Number of heat wave per year:', len(durations)/num_years)

    return durations, df


if __name__ == '__main__':

    filelist = glob.glob('T*.csv')
    f = 'Tx_R3.txt'
    sta, dfn = ReadInputTXTFiles(f)

    for f in filelist:
        # Doc du lieu tu file        
        df = ReadInputCSVFiles(f)
        
        # Xac dinh heat wave
        durations, df2  = HeatWaveIdentification(df,'MAX_TMP',0.9)


    #df = pd.read_fwf('Tx_R3.txt',skiprows=1121,nrows=500)
#     y=a*x+b
#     plt.figure()
#     plt.plot(R_ann,'o')
#     plt.plot(x,y,ls='-')
#     plt.title(file)
#     plt.figure()
#     plt.plot(x, R_ann,'o')
#     plt.plot(x, res[1] + res[0] * x, 'r-')
#     plt.plot(x, res[1] + res[2] * x, 'r--')
#     plt.plot(x, res[1] + res[3] * x, 'r--')
#     plt.plot(x, lsq_res[1] + lsq_res[0] * x, 'g-')
#     plt.title(file)
# plt.plot(df_tram['rainfall'].values)
# plt.show()
