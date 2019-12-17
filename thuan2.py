import pandas as pd
import datetime 
from itertools import islice
import matplotlib.pyplot as plt

#INPUTFILE = 'Tx_R3.txt'

if __name__ == '__main__':
    #read file, split to trunk  
    dict_hwn = dict() #heatwave number dictionary, key is station name, value = array of year value
    dict_threshold = dict()

    with open('Tx_R3.txt') as f:
        while True:
            station_info = f.readline()
            if station_info == '':
                break
            station = station_info.split()[0]   #name of station
            #extract station information here
            dict_hwn[station] = list()
            df = pd.DataFrame()

            for year in range(1980, 2015):
                chunk = list(islice(f, 32))
                datayear = dict()
                # print(chunk)
                
                #analyse data of year of that station here
                year = chunk[0].split()[0]
                run_date = datetime.date(int(year), 1, 1)
                end_date = datetime.date(int(year), 12, 31)
                while run_date <= end_date:
                    datayear[run_date] = float(chunk[run_date.day].split()[run_date.month])
                    run_date += datetime.timedelta(days=1)
                dfyear = pd.DataFrame.from_dict(datayear, orient='index', columns=['temp'])
                fdate = datetime.date(int(year), 4, 1) 
                edate = datetime.date(int(year), 9, 30)
                df49 = dfyear[fdate:edate]
                df.append(df49)

            # print(datayear)
            # print(dfyear_took)
            hw_thres = df['temp'].quantile(0.9)
            dict_threshold[station] = hw_thres
            # print('thres:', hw_thres)            
            # HEATWAVE DETECTION
            # tag rows based on the threshold
            df['tag'] = df['temp'] > hw_thres
            # first row is a True preceded by a False (first month of an event)
            fst = df.index[df['tag'] & ~ df['tag'].shift(1).fillna(False)]
    
            # last row is a True followed by a False (last month of an event)
            lst = df.index[df['tag'] & ~ df['tag'].shift(-1).fillna(False)]

            durations = list((lst[i] - fst[i]).days for i in range(min(len(lst), len(fst))))
            #remove the duration value < 3
            durations3 = [i for i in durations if i >= 3]
            #them so lan heatwave vao dictionary
            dict_hwn[station].append(len(durations3))

    # print(dict_hwn)
    #plot things
    plt.plot(dict_hwn["HANOI"])
    plt.show()


#dict_hwn {"name": array of hwn }
#dict_hwd
#dict_hwf
