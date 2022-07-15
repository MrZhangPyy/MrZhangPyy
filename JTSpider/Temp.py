import pandas as pd
import numpy as np

df = pd.read_excel('com_juping.xlsx')
df = pd.DataFrame(df)
df.apply(lambda s:s.groupby(s.le(0).cumsum).agg(['count','sum']).loc[lambda d:d.count>2,'sum'].sum())
