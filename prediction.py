import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')
from datetime import datetime, timedelta

import warnings as warnings
warnings.filterwarnings("ignore")
import FinanceDataReader as fdr

df = pd.read_csv('BTC_USDT_5m.csv')
df.columns = ['Date', 'Open','High','Low','Close','Volume']
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df['Return'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1)) * 100
df.dropna(inplace=True)

df['Status'] = np.where((df.Close.shift(2) < df.Close.shift(1)) & (df.Close.shift(1) < df.Close),1,0)
print(df)