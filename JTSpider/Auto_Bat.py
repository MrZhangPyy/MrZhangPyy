import requests
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import numpy as np

def main(routename):
    authtoken = '5914f308417840fdbda37d3dc8e4b7a8'
    global headers
    headers = {
        'authority': 'jmsgw.jtexpress.com.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authtoken': authtoken,
        'cache-control': 'max-age=2, must-revalidate',
        'content-type': 'application/json;charset=UTF-8',
        'lang': 'zh_CN',
        'origin': 'https://jms.jtexpress.com.cn',
        'referer': 'https://jms.jtexpress.com.cn/',
        'routename': routename,
        'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    return headers
'''
请求头生成器
'''
def get_time_now():
    global startDates,endDates
    time_now_stamp = int(time.time())
    startDates = str(datetime.fromtimestamp(time_now_stamp - 9600))
    endDates = str(datetime.fromtimestamp(time_now_stamp - 8400))
    print(startDates, endDates)
    return startDates,endDates
'''
时间模块
'''
def yfwd(startDates,endDates):
    routename = 'newArriveMonitor'
    main(routename)
    global waybillNoPool
    waybillNoPool = []
    pre_data = {"current":1,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002","exportType":6,"type":6,"countryId":"1"}
    first_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',headers=headers, json=pre_data).json()
    max_pages = first_req['data']['pages'] + 1
    for pages in range(1, max_pages):
        data = {"current":pages,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002","exportType":6,"type":6,"countryId":"1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',headers=headers, json=data).json()
        response = response['data']['records']
        for dic in tqdm(response):
            if dic.get('packageNumber') is None:
                pass
            elif dic.get('packageNumber')[0] == "B":
                waybillNo = dic.get('billCode')
                waybillNoPool.append(waybillNo)
    return waybillNoPool
'''
从到件监控系统构建单号池
'''
def data_wash(waybillNoPool):
    routename = 'scanQueryConstantlyNew'
    main(routename)
    count = (len(waybillNoPool) - 1) // 200 + 1
    billNoFinal = pd.DataFrame()
    for i in range(count):
        ifrom = i * 200
        ito = ifrom + 200
        pre_data = {"current": 1, "size": 1000, "startDates": "2022-07-13 00:00:00", "endDates": "2022-07-13 23:59:59","scanType": "全部", "sortName": "scanDate", "sortOrder": "desc", "bilNos": waybillNoPool[ifrom:ito],"queryTerminalDispatchCode": 0, "querySub": "", "reachAddressCodeList": [], "sendSites": [],"billType": 1, "countryId": "1"}
        pre_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',headers=headers, json=pre_data).json()
        max_pages = pre_req["data"]["pages"]
        billNoSum = pd.DataFrame()
        for pages in range(1, max_pages):
            data = {"current": pages, "size": 1000, "startDates": "2022-07-13 00:00:00","endDates": "2022-07-13 23:59:59", "scanType": "全部", "sortName": "scanDate", "sortOrder": "desc","bilNos": waybillNoPool[ifrom:ito], "queryTerminalDispatchCode": 0, "querySub": "","reachAddressCodeList": [], "sendSites": [], "billType": 1, "countryId": "1"}
            response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',headers=headers, json=data).json()
            billNoTemp = pd.DataFrame(response["data"]["records"])
            billNoTemp = billNoTemp[['billNo', 'belongNo', 'scanType', 'scanDate', 'inputDept']]
            billNoTemp.dropna(subset=['belongNo'], inplace=True)
            billNoSum = pd.concat([billNoSum, billNoTemp])
        billNoFinal = pd.concat([billNoFinal, billNoSum])
    billNoFinal['scanDate'] = pd.to_datetime(df.scanDate)
    billNoFinal.sort_values('scanDate', ascending = False, inplace = True)
    print(billNoFinal)
    billNoFinal.to_excel("TEST.xlsx", index=False)
    print(">>>>>>Finished!<<<<<<")
    return billNoFinal
'''
数据清洗
'''
def send_Requests():
    pass
'''
发送数据
'''
if __name__ == '__main__':
    while True:
        # get_time_now()
        startDates = "2022-07-13 04:00:00"
        endDates = "2022-07-13 04:20:00"
        yfwd(startDates,endDates)
        data_wash(waybillNoPool)
        print(">>>>>>Waiting!<<<<<<")
        time.sleep(12000)
