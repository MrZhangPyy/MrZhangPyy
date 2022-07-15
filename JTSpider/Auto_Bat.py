import copy

import requests
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import numpy as np

'''
*Headers generator;
'''
def headers_generator(routename):
    authtoken = 'a80863fcd74c4768ab3d51949aa2ed43'
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
*Time module;
'''
def get_time_now():
    global startDates,endDates
    time_now_stamp = int(time.time())
    startDates = str(datetime.fromtimestamp(time_now_stamp - 9600))
    endDates = str(datetime.fromtimestamp(time_now_stamp - 8400))
    print(startDates, endDates)
    return startDates,endDates

'''
*Package number checker and filter;
'''
def packageNum_check(packageNum_list):
    routename = 'electronicPackagePrinting'
    headers_generator(routename)
    data = {"current":1,"size":20,"startCreateTime":"2022-07-15 00:00:00","endCreateTime":"2022-07-15 23:59:59",
     "createNetworkCode":"0711002","packageNumberList":packageNum_list,"countryId":"1"}
    response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                             headers=headers,json=data).json()
    response = response['data']['records']
    for dic in response:
        if dic.get('packageCode') == "501" and (dic.get('createNetworkCode') == "502701B1" or dic.get('createNetworkCode') == "502701"):
            pass
        else:packageNum_list.remove(dic.get('packageNumber'))
    return packageNum_list

'''
*Constuct bill code pool from system to be further handling;
'''
def yfwd(startDates,endDates):
    routename = 'newArriveMonitor'
    headers_generator(routename)
    temp_dic = {}
    packageNum_list = []
    global waybillNo_Pool
    waybillNo_Pool = []
    pre_data = {"current":1,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002",
                "exportType":6,"type":6,"countryId":"1"}
    first_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',
                              headers=headers, json=pre_data).json()
    max_pages = first_req['data']['pages'] + 1
    for pages in range(1, max_pages):
        data = {"current":pages,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002",
                "exportType":6,"type":6,"countryId":"1"}
        response1 = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',
                                 headers=headers, json=data).json()
        response1 = response1['data']['records']
        for dic1 in tqdm(response1):
            if dic1.get('packageNumber') is None:
                pass
            elif dic1.get('packageNumber')[0] == "B":
                temp_dic['运单号'] = dic1.get('billCode')
                temp_dic['包号'] = dic1.get('packageNumber')
                waybillNo_Pool.append(copy.deepcopy(temp_dic))
                if dic1.get('packageNumber') in packageNum_list:
                    pass
                else:packageNum_list.append(dic1.get('packageNumber'))
    print(waybillNo_Pool)
    print(packageNum_list)
    waybillNo_Pool = pd.DataFrame(waybillNo_Pool)
    routename = 'electronicPackagePrinting'
    headers_generator(routename)
    data = {"current": 1, "size": 20, "startCreateTime": "2022-07-15 00:00:00", "endCreateTime": "2022-07-15 23:59:59",
            "createNetworkCode": "0711002", "packageNumberList": packageNum_list, "countryId": "1"}
    response2 = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                             headers=headers, json=data).json()
    response2 = response2['data']['records']
    for dic2 in response2:
        if dic2.get('packageCode') == "501" and (dic2.get('createNetworkCode') == "502701B1" or dic2.get('createNetworkCode') == "502701"):
            pass
        else:packageNum_list.remove(dic2.get('packageNumber'))
    print(packageNum_list)
    waybillNo_Pool[waybillNo_Pool["包号"].isin(packageNum_list)]
    return waybillNo_Pool

'''
*Data wash and save to xlsx file;
'''
def data_wash(waybillNoPool):
    routename = 'scanQueryConstantlyNew'
    headers_generator(routename)
    count = (len(waybillNoPool) - 1) // 200 + 1
    billNoFinal = pd.DataFrame()
    for i in range(count):
        ifrom = i * 200
        ito = ifrom + 200
        pre_data = {"current": 1, "size": 1000, "startDates": "2022-07-13 00:00:00", "endDates": "2022-07-13 23:59:59",
                    "scanType": "全部", "sortName": "scanDate", "sortOrder": "desc", "bilNos": waybillNoPool[ifrom:ito],
                    "queryTerminalDispatchCode": 0, "querySub": "", "reachAddressCodeList": [], "sendSites": [],
                    "billType": 1, "countryId": "1"}
        pre_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                                headers=headers, json=pre_data).json()
        max_pages = pre_req["data"]["pages"]
        billNoSum = pd.DataFrame()
        for pages in range(1, max_pages):
            data = {"current": pages, "size": 1000, "startDates": "2022-07-13 00:00:00",
                    "endDates": "2022-07-13 23:59:59", "scanType": "全部", "sortName": "scanDate", "sortOrder": "desc",
                    "bilNos": waybillNoPool[ifrom:ito], "queryTerminalDispatchCode": 0, "querySub": "",
                    "reachAddressCodeList": [], "sendSites": [], "billType": 1, "countryId": "1"}
            response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                                     headers=headers, json=data).json()
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
*Send xlsx file via requests.post to server.
'''
def send_Requests():
    pass

if __name__ == '__main__':
    while True:
        # get_time_now()
        startDates = "2022-07-15 22:31:54"
        endDates = "2022-07-15 22:31:56"
        yfwd(startDates,endDates)
        # print(waybillNo_Pool)
        # data_wash(waybillNoPool)
        print(">>>>>>Waiting Now!<<<<<<")
        time.sleep(12000)
