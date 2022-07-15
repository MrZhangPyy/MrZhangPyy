import time
from datetime import datetime

a = "2022-07-07 14:26:17"
time_Hour = datetime.fromtimestamp(int(time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S")))).strftime('%H')
print(time_Hour)
