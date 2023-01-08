from datetime import datetime,timedelta
import MetaTrader5 as mt5 
import pandas as pd

def box():
    mt5.initialize()

    SYMBOLS = ["USDJPY.p","CADJPY.p","AUDJPY.p","CHFJPY.p","GBPJPY.p","EURJPY.p","NZDJPY.p","USOUSD.p","XAUUSD.p","DJ30.s","NAS100.s","SP500.s","DAX40.s"]
    NOW = datetime.today() + timedelta(hours=2)
    LASTDAY = NOW - timedelta(days=1)
    LASTDAY = LASTDAY.replace(hour=23, minute=00)
    TF = mt5.TIMEFRAME_M30
    list_cur = []
    for symbol in SYMBOLS:
        TP = 0
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
            TP = Min - abs(Max-Min)
        elif (pd.Series(df1[:1].close.astype(float) < df2[:1].close.astype(float)).bool()): #UP
            direction = 'UpTrend'
            TP = Max + abs(Max-Min)

        
        list_cur.append(f'{symbol}, {direction}, Max: {Max}, Min: {Min}, PIP: {round(round(abs(Max-Min),2)*100,2)}, TP: {round(TP,3)}')
    mt5.shutdown()
    return list_cur