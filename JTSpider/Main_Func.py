import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
from datetime import datetime
import copy

'''
*Headers generator;
'''
def headers_generator(authtoken = "",routename = ""):
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    return headers

'''
Gathering wrong dispatch raw data;
'''
def fetch_wrong():
    print("Gathering wrong dispatch raw data...")
    date = input("请输入日期：\neg：2022-07-22")
    startTime = date + " 00:00:00"
    endTime = date + " 23:59:59"
    data = {"current": 1,
            "size": 500,
            "receiveNetworkId": 20024,
            "problemTypeSubjectCodeList": ["23", "31"],
            "isRegistration": 2,
            "startTime": startTime,
            "endTime": endTime,
            "receiveNetworkProxyCodes": [],
            "regNetworkProxyCodes": [],
            "waybillType": "1",
            "countryCode": "CN",
            "countryId": "1"
            }
    response = requests.post('https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/monitorPage', headers=headers,
                             json=data).json()
    print("Gathering wrong dispatch raw data finished...")

'''
Wrong dispatch raw data further operating;
'''
def wrong_dispatch(单号池 = []):
    print("Wrong dispatch raw data further operating...")
    routename = "trackingExpress"
    headers_generator(authtoken,routename)
    list_result = []
    for waybillNo in raw_List:
        data = {"waybillNo": waybillNo, "countryId": "1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/order/getOrderDetail',
                                 headers=headers, json=data).json()
        destination = response['data']['details']['dispatchNetworkName']
        dic_result['运单号'] = waybillNo
        dic_result['系统正确网点'] = destination
        data = {"keywordList": [waybillNo], "trackingTypeEnum": "WAYBILL", "countryId": "1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/podTracking/inner/query/keywordList',
                                 headers=headers, json=data).json()
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
            time_Hour = int(datetime.fromtimestamp(
                int(time.mktime(time.strptime(dic_result.get('扫描时间'), "%Y-%m-%d %H:%M:%S")))).strftime('%H'))
            if "君润" in dic_result.get('责任人'):
                if (time_Hour > 10 or time_Hour == 10) and time_Hour < 20:
                    dic_result['班次'] = "白"
                else:
                    dic_result['班次'] = "夜"
            else:
                dic_result['班次'] = ""
        else:
            dic_result['班次'] = ""
        list_result.append(copy.deepcopy(dic_result))


'''
*Time module;
'''
def time_module(i):
    global Dates
    Dates = str(datetime.fromtimestamp(i))
    return Dates

'''
*Package number checker and filter;
'''
def packageNum_check(packageNum_List = []):
    print("Package number check...")
    global waybillNo_Pool
    if len(packageNum_List) > 0:
        routename = 'electronicPackagePrinting'
        headers_generator(authtoken,routename)
        data = {"current":1,"size":1000,"startCreateTime":"2022-07-15 00:00:00","endCreateTime":"2022-07-15 23:59:59",
         "createNetworkCode":"0711002","packageNumberList":packageNum_List,"countryId":"1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                                 headers=headers,json=data).json()
        response = response['data']['records']
        for dic in response:
            if not (dic.get('packageCode') == "501" and (dic.get('createNetworkCode') == "502701B1" or dic.get('createNetworkCode') == "502701")):
                packageNum_List.remove(dic.get('packageNumber'))
            else:pass
        waybillNo_Pool = waybillNo_Pool[waybillNo_Pool["包号"].isin(packageNum_List)]
    else:pass
    print("Package number check finished...")
    return waybillNo_Pool

'''
*Constuct bill code pool from system to be further handling;
'''
def not_actually_arrived(startDates = "",endDates = ""):
    print("开始时间：{}，结束时间：{}.".format(startDates,endDates))
    print("Gathering data...")
    routename = 'newArriveMonitor'
    headers_generator(authtoken,routename)
    temp_dic = {}
    packageNum_List = []
    global waybillNo_Pool,waybillNo_List
    waybillNo_Pool = []
    pre_data = {"current":1,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002",
                "exportType":6,"type":6,"countryId":"1"}
    first_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',
                              headers=headers, json=pre_data).json()
    max_pages = first_req['data']['pages'] + 1
    for pages in tqdm(range(1, max_pages)):
        data = {"current":pages,"size":1000,"startDates":startDates,"endDates":endDates,"siteCode":"0711002",
                "exportType":6,"type":6,"countryId":"1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',
                                 headers=headers, json=data).json()
        response = response['data']['records']
        for dic in response:
            if dic.get('packageNumber') is None:
                pass
            elif dic.get('packageNumber')[0] == "B":
                temp_dic['运单号'] = dic.get('billCode')
                temp_dic['包号'] = dic.get('packageNumber')
                waybillNo_Pool.append(copy.deepcopy(temp_dic))
                if dic.get('packageNumber') in packageNum_List:
                    pass
                else:packageNum_List.append(dic.get('packageNumber'))
    waybillNo_Pool = pd.DataFrame(waybillNo_Pool)
    print("Gathering data finished...")
    packageNum_check(packageNum_List)
    waybillNo_List = waybillNo_Pool['运单号'].tolist()
    return waybillNo_List

'''
*Data wash and save to xlsx file;
'''
def data_wash(waybillNo_List = []):
    print("Data washing...")
    routename = 'scanQueryConstantlyNew'
    headers_generator(authtoken,routename)
    count = (len(waybillNo_List) - 1) // 200 + 1
    global billNoFinal
    billNoFinal = pd.DataFrame()
    for i in tqdm(range(count)):
        ifrom = i * 200
        ito = ifrom + 200
        pre_data = {"current": 1, "size": 1000, "startDates": "2022-07-13 00:00:00", "endDates": "2022-07-13 23:59:59",
                    "scanType": "全部", "sortName": "scanDate", "sortOrder": "desc", "bilNos": waybillNo_List[ifrom:ito],
                    "queryTerminalDispatchCode": 0, "querySub": "", "reachAddressCodeList": [], "sendSites": [],
                    "billType": 1, "countryId": "1"}
        pre_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                                headers=headers, json=pre_data).json()
        max_pages = pre_req["data"]["pages"] + 1
        billNoSum = pd.DataFrame()
        for pages in range(1, max_pages):
            data = {"current": pages, "size": 1000, "startDates": "2022-07-13 00:00:00",
                    "endDates": "2022-07-13 23:59:59", "scanType": "全部", "sortName": "scanDate", "sortOrder": "desc",
                    "bilNos": waybillNo_List[ifrom:ito], "queryTerminalDispatchCode": 0, "querySub": "",
                    "reachAddressCodeList": [], "sendSites": [], "billType": 1, "countryId": "1"}
            response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                                     headers=headers, json=data).json()
            billNoTemp = pd.DataFrame(response["data"]["records"])
            billNoTemp = billNoTemp[['billNo', 'belongNo', 'scanType', 'scanDate', 'inputDept']]
            billNoTemp.dropna(subset=['belongNo'], inplace=True)
            billNoSum = pd.concat([billNoSum, billNoTemp])
        billNoFinal = pd.concat([billNoFinal, billNoSum])
    if not billNoFinal.empty:
        billNoFinal['scanDate'] = pd.to_datetime(billNoFinal['scanDate'])
        billNoFinal.sort_values('scanDate',ascending=False,inplace=True)
        billNoFinal.drop_duplicates(subset="billNo",keep='first',inplace=True)
        billNoFinal = billNoFinal[billNoFinal["inputDept"].isin(["鄂州葛店集散点"])]
        billNoFinal = billNoFinal[billNoFinal["scanType"].isin(["到件扫描","卸车扫描"])]
        billNoFinal.drop(['belongNo', 'scanType', 'scanDate', 'inputDept'], axis=1, inplace=True)
        billNoFinal.rename(columns={'billNo':'运单号'},inplace=True)
        billNoFinal.insert(billNoFinal.shape[1], '操作类型', "转运")
        billNoFinal.insert(billNoFinal.shape[1], '问题件一级类型', "有发未到件")
        billNoFinal.insert(billNoFinal.shape[1], '问题件二级类型', "有发未到件a")
        billNoFinal.insert(billNoFinal.shape[1], '问题件原因', "此件为包内件，路由显示发往我司，但实际并未到达！")
    else:print("无待处理数据！")
    print(billNoFinal)
    print("Data washing finished...")
    return

'''
*Send xlsx file via requests.post to server.
'''
def send_Requests(authtoken = "",file_path =""):
    print("Sending requests to server...")
    billNoFinal.to_excel("有发未到模板.xlsx", index=False)
    headers = {
            'authority': 'jmsgw.jtexpress.com.cn',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authtoken': authtoken,
            'cache-control': 'max-age=2, must-revalidate',
            'lang': 'zh_CN',
            'origin': 'https://jms.jtexpress.com.cn',
            'referer': 'https://jms.jtexpress.com.cn/',
            'routename': 'batchProblem',
            'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '^\\^Windows^\\^',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
    payload = """------WebKitFormBoundaryS9oPPAFn1ng8pW13
                 Content-Disposition: form-data; name="uploadFile"; filename="有发未到模板.xlsx"
                 Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
                 ------WebKitFormBoundaryS9oPPAFn1ng8pW13--"""
    data = {"uploadFile" : open(file_path,"rb")}
    url = "https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/import"
    res = requests.post(url,headers = headers,files=data).json()
    print("Sending requests to server finished...")
    print("Final result:",res['msg'])

if __name__ == '__main__':
    authtoken = '2c70ab6ae3f7404385ec64cfb28eb9bf'
    while True:
        print('请输入需要使用的功能编号：\n1.自动有发未到；\n2.错分数据导出&自动分析；\n(输入“#”以退出！)')
        in_put = input(">>>")
        if in_put == "1":
            stamp = int(time.time()) - 6900
            while True:
                startDates = "2022-07-21 17:00:00"
                endDates = "2022-07-21 17:10:00"
                # startDates = time_module(stamp)
                # endDates = time_module(stamp + 1200)
                # stamp += 1201
                not_actually_arrived(startDates,endDates)
                data_wash(waybillNo_List)
                # send_Requests(authtoken,"./有发未到模板.xlsx")
                print("ALL DONE ! Next operation coming soon......")
                time.sleep(1200)
        elif in_put == "2":
            fetch_wrong()
            wrong_dispatch()
            pass
        elif in_put.strip() == "#":
            pass
