import requests
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime

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

def gettime_now():
    global startDates,endDates
    time_now_stamp = int(time.time())
    startDates = str(datetime.fromtimestamp(time_now_stamp - 9600))
    endDates = str(datetime.fromtimestamp(time_now_stamp - 8400))
    return startDates,endDates

def yfwd(startDates,endDates):
    global waybillNo_Pool,lenth
    waybillNo_Pool = []
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
                waybillNo_Pool.append(waybillNo)
    lenth = len(waybillNo_Pool)
    return waybillNo_Pool,lenth

def pre_request(headers, shipmentNo, page):
    params = {"current": page,"size": 1000,"shipmentNo": shipmentNo,"scanNetworkCode": "502701B1"}
    temp_list = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/page',headers=headers, params=params).json()
    return temp_list["data"]["pages"]

def fetchingwrong(date):

    data = {"current":1,
         "size":20,
         "receiveNetworkId":20024,
         "problemTypeSubjectCodeList":["23","31"],
         "isRegistration":2,
         "startTime":"2022-07-09 00:00:00",
         "endTime":"2022-07-09 23:59:59",
         "receiveNetworkProxyCodes":[],
         "regNetworkProxyCodes":[],
         "waybillType":"1",
         "countryCode":"CN",
         "countryId":"1"
         }
    response = requests.post('https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/monitorPage', headers=headers, json=data).json()
    print(response)

def wrongdispatch(waybillNo):
    global dic_result
    data = {"waybillNo": waybillNo,"countryId": "1"}
    response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/order/getOrderDetail',headers=headers,json=data).json()
    destination = response['data']['details']['dispatchNetworkName']
    dic_result['运单号'] = waybillNo
    dic_result['系统正确网点'] = destination
    data = {"keywordList": [waybillNo],"trackingTypeEnum": "WAYBILL","countryId": "1"}
    response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/podTracking/inner/query/keywordList',headers=headers,json=data).json()
    response = response["data"][0]['details']
    true_index = len(response)
    for dic in response:
        temp1 = dic.get('scanTypeName')
        temp2 = dic.get("remark1")
        if temp1 == "问题件扫描" and ("错分" in temp2 or "错发" in temp2):
            dic_result['登记网点'] = dic.get('scanNetworkName')
            wrong_index = response.index(dic) + 1
            break
    if dic_result.get('系统正确网点') == dic_result.get('登记网点'):
        dic_result['是否网点错报'] = 1
    else:
        dic_result['是否网点错报'] = 0
        for i in range(wrong_index, true_index):
            dic = response[i]
            temp4 = dic.get('scanNetworkName')
            if temp4 == "鄂州葛店集散点":
                temp5 = dic.get('scanTypeName')
                if temp5 == "装车发件":
                    temp6 = dic.get('nextStopName')
                    if temp6 == dic_result.get('登记网点') and temp6 != dic_result['系统正确网点']:
                        dic_result['错分类型'] = '发件扫描'
                        dic_result['责任人'] = dic.get('scanByName')
                        dic_result['扫描时间'] = dic.get('scanTime')
                        break
                        # 发件扫描
                    elif temp6 != dic_result.get('登记网点'):
                        dic_result['错分类型'] = '错装车'
                        dic_result['责任人'] = '君润'
                        dic_result['扫描时间'] = dic.get('scanTime')
                        break
                        # 错装车
                elif temp5 == "卸车到件" or temp5 == "集货到件":
                    dic_result['错分类型'] = '漏扫错分'
                    dic_result['责任人'] = '君润'
                    dic_result['扫描时间'] = ''
                    break
                    # 漏扫错分
    if dic_result.get('是否网点错报') == 0 and dic_result.get('扫描时间') != "":
        time_Hour = int(datetime.fromtimestamp(int(time.mktime(time.strptime(dic_result.get('扫描时间'), "%Y-%m-%d %H:%M:%S")))).strftime('%H'))
        if "君润" in dic_result.get('责任人'):
            if (time_Hour > 10 or time_Hour ==10) and time_Hour < 20:
                dic_result['班次'] = "白"
            else: dic_result['班次'] = "夜"
        else:dic_result['班次'] = ""
    else:dic_result['班次'] = ""
    return dic_result

def getbillinfo(waybillNo_Pool):
    for waybillNo in waybillNo_Pool:

        pass

if __name__ == '__main__':
    routename = 'newArriveMonitor'
    main(routename)
    while True:
        gettime_now()
        yfwd(startDates,endDates)
        data_wash(waybillNo_Pool)
        print(billNoFinal)
        time.sleep(1200)
    pass
