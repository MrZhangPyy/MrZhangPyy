import requests
import pandas as pd
from tqdm import *
import time
from datetime import datetime

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': 'dd2c597c6ee54b3db6a782f9ad6adcba',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'newArriveMonitor',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
list_result = []
dic_result = {}
data1 = {"current":1,"size":1000,"startDates":"2022-07-12 17:00:00","endDates":"2022-07-12 18:59:59","siteCode":"0711002","exportType":6,"type":6,"countryId":"1"}
first_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail', headers=headers, json=data1).json()
max_pages = first_req['data']['pages']+1
start_time = time.time()
for page in tqdm(range(1,max_pages)):
    data = {"current":page,"size":1000,"startDates":"2022-07-12 17:00:00","endDates":"2022-07-12 18:59:59","siteCode":"0711002","exportType":6,"type":6,"countryId":"1"}
    response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail', headers=headers, json=data).json()
    response = response['data']['records']
    for dic in tqdm(response):
        dic_result['运单编号'] = dic.get('billCode')
        dic_result['包号'] = dic.get('packageNumber')
        dic_result['到件时间'] = dic.get('arriveTime')
        list_result.append(dic_result.copy())
df_data = pd.DataFrame.from_dict(list_result)
df_data.dropna(subset=['包号'], inplace=True)
df_data.to_excel("Test1.xlsx", index=False)
end_time = time.time()
print("耗时：{}秒。".format(end_time - start_time))
