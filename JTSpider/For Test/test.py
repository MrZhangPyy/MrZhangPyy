import requests
import pandas as pd
from time import *
from threading import Thread
from queue import Queue
import numpy as np

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '9dfb812c11a24168bcf49718888ffd8a',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'scanQueryConstantlyNew',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}


page = 1
pre_pay_load = {"current": page,
                "size": 1000,
                "startDates": "2022-05-14 10:00:00",
                "endDates": "2022-05-14 12:00:00",
                "scanSite": "0711002",
                "scanType": "发件扫描",
                "filterNo": "2",
                "sortName": "scanDate",
                "sortOrder": "desc",
                "bilNos": [],
                "queryTerminalDispatchCode": 0,
                "querySub": "",
                "reachAddressList": [],
                "sendSites": [],
                "billType": 1,
                "countryId": "1"
                }


begin_time = time()
raw_res = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',headers=headers,json=pre_pay_load).json()
bill_count = raw_res["data"]["total"]
max_page = raw_res["data"]["pages"]
list_result = []
df_result = pd.DataFrame()
for page in range(max_page):
    data = {"current": page,
            "size": 1000,
            "startDates": "2022-05-14 10:00:00",
            "endDates": "2022-05-14 12:00:00",
            "scanSite": "0711002",
            "scanType": "发件扫描",
            "filterNo": "2",
            "sortName": "scanDate",
            "sortOrder": "desc",
            "bilNos": [],
            "queryTerminalDispatchCode": 0,
            "querySub": "",
            "reachAddressList": [],
            "sendSites": [],
            "billType": 1,
            "countryId": "1"
            }
    temp_list = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',headers=headers,json=data).json()
    temp_df = pd.DataFrame(temp_list["data"]["records"])
    df_result = pd.concat([df_result, temp_df])


data_gathering_ended_time = time()
gathering_time_cost = data_gathering_ended_time - begin_time
print("数据读取完毕，耗时", gathering_time_cost, "秒。")


df_result.to_excel("test.xlsx", index=False)
data_saving_ended_time = time()
saving_time_cost = data_saving_ended_time - data_gathering_ended_time
print("数据写入完毕，耗时", saving_time_cost, "秒。")


total_time_cost = data_saving_ended_time - begin_time
print("程序结束，", bill_count, "行数据已保存，总计耗时：", total_time_cost, "秒！")
