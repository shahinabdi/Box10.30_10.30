from datetime import datetime,timedelta
import MetaTrader5 as mt5 
import pandas as pd

def box():
    mt5.initialize()

    SYMBOLS = ["USDJPY.p","CADJPY.p","AUDJPY.p","CHFJPY.p","GBPJPY.p","EURJPY.p","NZDJPY.p","USOUSD.p"]
    NOW = datetime.today()
    LASTDAY = NOW - timedelta(days=1)
    TF = mt5.TIMEFRAME_M30
    list_cur = []
    for symbol in SYMBOLS:
        bars = mt5.copy_rates_range(symbol, TF, LASTDAY,NOW)
        df = pd.DataFrame(bars)[['time', 'open','high', 'low','close']]
        df['time'] = pd.to_datetime(df.time, unit='s')
        df1 = df[df.time.astype(str).str[-8:] == '23:30:00'].reset_index()[['time','close']]
        df2 = df[df.time.astype(str).str[-8:] == '11:30:00'].reset_index()[['time', 'close']]

        idx_23 = df.index[df.time.astype(str).str[-8:] == '23:30:00'].tolist()
        idx_11 = df.index[df.time.astype(str).str[-8:] == '11:30:00'].tolist()
        Max = df[idx_23[0]:idx_11[0]+1].high.max()
        Min = df[idx_23[0]:idx_11[0]+1].low.min()

        if (pd.Series(df1[:1].close.astype(float) > df2[:1].close.astype(float)).bool()): #Down
            direction = 'DownTrend'
        elif (pd.Series(df1[:1].close.astype(float) < df2[:1].close.astype(float)).bool()): #UP
            direction = 'UpTrend'
        
        list_cur.append(f'{symbol}, {direction}, Max: {Max}, Min: {Min}, PIP: {round(round(abs(Max-Min),2)*100,2)}')
    mt5.shutdown()
    return list_cur