import copy
import requests
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import numpy as np

def time_module(i):
    global Dates
    Dates = str(datetime.fromtimestamp(i))
    return Dates

if __name__ == '__main__':
    stamp = int(time.time()) - 5400
    while True:
        startDates = time_module(stamp)
        endDates = time_module(stamp + 1200)
        print(startDates,endDates)
        # startDates = "2022-07-16 00:28:00"
        # endDates = "2022-07-16 00:29:00"
        # not_actually_arrived(startDates,endDates)
        stamp += 1201
        print(">>>>>>Waiting Now!<<<<<<")
        time.sleep(1200)
