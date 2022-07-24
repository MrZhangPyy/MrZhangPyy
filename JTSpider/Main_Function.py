import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
from datetime import datetime
import copy


def headers_generator(authtoken="", routename=""):
    '''
    *Headers generator;
    '''
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


def vehicle_info(Start="", End=""):
    '''
    *Vehicle infomation export;
    '''
    headers1 = headers_generator(authtoken, 'brancTaskTrackSearch')
    headers2 = headers_generator(authtoken, 'brancTaskTrackSearchView')
    headers3 = headers_generator(authtoken, 'monitoringSearch')
    headers4 = headers_generator(authtoken, 'monitoringSearchView')
    load_type = {"current": 1, "size": 100, "startDepartureTime": Start + " 10:00:00",
                 "endDepartureTime": End + " 10:00:00", "startActualDepartureTime": Start + " 10:00:00",
                 "endActualDepartureTime": End + " 10:00:00", "startCode": "0711002", "shipmentState": 4,
                 "countryId": "1"}
    unload_type = {"current": 1, "size": 100, "startDepartureTime": Start + " 10:00:00",
                   "endDepartureTime": End + " 10:00:00", "startActualDepartureTime": Start + " 10:00:00",
                   "endActualDepartureTime": End + " 10:00:00", "endCode": "0711002", "shipmentState": 4,
                   "countryId": "1"}
    response1 = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page',
                              headers=headers,
                              json=load).json()
    response1 = response1["data"]["records"]
    list_ = []
    for dic in tqdm(response1):
        dic_new = {}
        dic_new["运输单号"] = dic["shipmentNo"]
        dic_new["始发转运"] = dic["startName"]
        dic_new["目的网点"] = dic["endName"]
        dic_new["线路方式"] = dic["startName"] + "-" + dic["endName"]
        dic_new["计划发车时间"] = dic["plannedDepartureTime"]
        dic_new["实际发车时间"] = dic["actualDepartureTime"]
        dic_new["车牌号"] = dic["plateNumber"]
        params = (('shipmentNo', dic["shipmentNo"]),)
        response2 = requests.get(
            'https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list',
            headers=headers2, params=params).json()
        dic_new["装载票数"] = response2["data"][0]["scanWaybillNum"]
        dic_new["车型"] = dic["actualVehicleTypegroup"]
        list_.append(copy.deepcopy(dic_new))

    response3 = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page',
                              headers=headers,
                              json=unload).json()
    response3 = response3["data"]["records"]
    list2_ = []
    for dic in tqdm(response3):
        dic_new = {}
        dic_new["运输单号"] = dic["shipmentNo"]
        dic_new["始发转运"] = dic["startName"]
        dic_new["目的网点"] = dic["endName"]
        dic_new["线路方式"] = dic["startName"] + "-" + dic["endName"]
        dic_new["计划到车"] = dic["plannedArrivalTime"]
        dic_new["实际到车"] = dic["actualArrivalTime"]
        dic_new["车牌号"] = dic["plateNumber"]
        params2 = (('shipmentNo', dic["shipmentNo"]),)
        response4 = requests.get(
            'https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list',
            headers=headers2, params=params2).json()
        dic_new["装载票数"] = response4["data"][0]["scanWaybillNum"]
        dic_new["车型"] = dic["actualVehicleTypegroup"]
        list2_.append(copy.deepcopy(dic_new))

    params3 = (
        ('current', '1'),
        ('size', '20'),
        ('startDateTime', '2022-07-23 10:00:00'),
        ('endDateTime', '2022-07-24 10:00:00'),
        ('gradeList', ''),
        ('searchType', 'manage'),
    )
    response5 = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsShipment/page', headers=headers3,
                             params=params3).json()
    response5 = response5["data"]["records"]
    list3_ = []
    for dic in tqdm(response5):
        dic_new = {}
        dic_new["运输单号"] = dic["shipmentNo"]
        dic_new["始发转运"] = dic["startName"]
        dic_new["目的地"] = dic["endName"]
        dic_new["线路方式"] = dic["shipmentName"]
        dic_new["计划发车"] = dic["plannedDepartureTime"]
        dic_new["实际发车"] = dic["actualDepartureTime"]
        dic_new["车牌号"] = dic["plateNumber"]
        params4 = (('shipmentNo', dic["shipmentNo"]),)
        response6 = requests.get('https://jmsgw.jtexpress.com.cn/transportation/trackingDeatil/loading/scan/list',
                                 headers=headers4, params=params4).json()
        response6 = response6["data"]
        for dic2 in response6:
            if dic2.get("loadingTypeName") == "装车扫描":
                dic_new["装载票数"] = dic2["scanWaybillNum"]
        dic_new["车型"] = dic["vehicleTypegroup"]
        list3_.append(copy.deepcopy(dic_new))

    list_ = pd.DataFrame(list_)
    list_.to_excel("离场.xlsx", index=False)
    list2_ = pd.DataFrame(list2_)
    list2_.to_excel("进场.xlsx", index=False)
    list3_ = pd.DataFrame(list3_)
    list3_.to_excel("干线.xlsx", index=False)


def fetch_wrong():
    '''
    Gathering wrong dispatch raw data;
    '''
    date = input("请输入日期：\n(eg：2022-07-22)\n")
    startTime = date + " 00:00:00"
    endTime = date + " 23:59:59"
    print("Gathering wrong dispatch raw data...")
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
    routename = 'problemPieceQueryCenter'
    headers_generator(authtoken, routename)
    response = requests.post('https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/monitorPage', headers=headers,
                             json=data).json()
    response = response['data']['records']
    global raw_list
    raw_list = []
    for dic in response:
        if dic.get('waybillNo') not in raw_list:
            raw_list.append(copy.deepcopy(dic.get('waybillNo')))
        else:
            pass
    print("Gathering wrong dispatch raw data finished...")


def wrong_dispatch(raw_list=[]):
    '''
    Wrong dispatch raw data further operating;
    '''
    print("Wrong dispatch raw data further operating...")
    routename = "trackingExpress"
    headers_generator(authtoken, routename)
    list_result = []
    for waybillNo in raw_list:
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


def time_module(i):
    '''
    *Time module;
    '''
    global Dates
    Dates = str(datetime.fromtimestamp(i))
    return Dates


def packageNum_check(packageNum_List=[]):
    '''
    *Package number checker and filter;
    '''
    print("Package number check...")
    global waybillNo_Pool
    if len(packageNum_List) > 0:
        routename = 'electronicPackagePrinting'
        headers_generator(authtoken, routename)
        data = {"current": 1, "size": 1000, "startCreateTime": "2022-07-15 00:00:00",
                "endCreateTime": "2022-07-15 23:59:59",
                "createNetworkCode": "0711002", "packageNumberList": packageNum_List, "countryId": "1"}
        response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                                 headers=headers, json=data).json()
        response = response['data']['records']
        for dic in response:
            if not (dic.get('packageCode') == "501" and (
                    dic.get('createNetworkCode') == "502701B1" or dic.get('createNetworkCode') == "502701")):
                packageNum_List.remove(dic.get('packageNumber'))
            else:
                pass
        waybillNo_Pool = waybillNo_Pool[waybillNo_Pool["包号"].isin(packageNum_List)]
    else:
        pass
    print("Package number check finished...")
    return waybillNo_Pool


def not_actually_arrived(startDates="", endDates=""):
    '''
    *Constuct bill code pool from system to be further handling;
    '''
    print("开始时间：{}，结束时间：{}.".format(startDates, endDates))
    print("Gathering data...")
    routename = 'newArriveMonitor'
    headers_generator(authtoken, routename)
    temp_dic = {}
    packageNum_List = []
    global waybillNo_Pool, waybillNo_List
    waybillNo_Pool = []
    pre_data = {"current": 1, "size": 1000, "startDates": startDates, "endDates": endDates, "siteCode": "0711002",
                "exportType": 6, "type": 6, "countryId": "1"}
    first_req = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail',
                              headers=headers, json=pre_data).json()
    max_pages = first_req['data']['pages'] + 1
    for pages in tqdm(range(1, max_pages)):
        data = {"current": pages, "size": 1000, "startDates": startDates, "endDates": endDates, "siteCode": "0711002",
                "exportType": 6, "type": 6, "countryId": "1"}
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
                else:
                    packageNum_List.append(dic.get('packageNumber'))
    waybillNo_Pool = pd.DataFrame(waybillNo_Pool)
    print("Gathering data finished...")
    packageNum_check(packageNum_List)
    waybillNo_List = waybillNo_Pool['运单号'].tolist()
    return waybillNo_List


def data_wash(waybillNo_List=[]):
    '''
    *Data wash and save to xlsx file;
    '''
    print("Data washing...")
    routename = 'scanQueryConstantlyNew'
    headers_generator(authtoken, routename)
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
        billNoFinal.sort_values('scanDate', ascending=False, inplace=True)
        billNoFinal.drop_duplicates(subset="billNo", keep='first', inplace=True)
        billNoFinal = billNoFinal[billNoFinal["inputDept"].isin(["鄂州葛店集散点"])]
        billNoFinal = billNoFinal[billNoFinal["scanType"].isin(["到件扫描", "卸车扫描"])]
        billNoFinal.drop(['belongNo', 'scanType', 'scanDate', 'inputDept'], axis=1, inplace=True)
        billNoFinal.rename(columns={'billNo': '运单号'}, inplace=True)
        billNoFinal.insert(billNoFinal.shape[1], '操作类型', "转运")
        billNoFinal.insert(billNoFinal.shape[1], '问题件一级类型', "有发未到件")
        billNoFinal.insert(billNoFinal.shape[1], '问题件二级类型', "有发未到件a")
        billNoFinal.insert(billNoFinal.shape[1], '问题件原因', "此件为包内件，路由显示发往我司，但实际并未到达！")
    else:
        print("无待处理数据！")
    print(billNoFinal)
    print("Data washing finished...")
    return


def send_Requests(authtoken="", file_path=""):
    '''
    *Send xlsx file via requests.post to server.
    '''
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
    data = {"uploadFile": open(file_path, "rb")}
    url = "https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/import"
    res = requests.post(url, headers=headers, files=data).json()
    print("Sending requests to server finished...")
    print("Final result:", res['msg'])


if __name__ == '__main__':
    authtoken = 'f96135b8a2d643ae8da327a4c925c192'  # Put validated token here.
    while True:
        print('请输入需要使用的功能编号：\n\n1.自动有发未到；\n\n2.错分数据导出 & 自动分析；\n\n3.车辆信息导出；\n\n(输入“#”以退出！)')
        in_put = input(">>>")
        if in_put == "1":
            stamp = int(time.time()) - 6900
            while True:
                startDates = "2022-07-21 17:00:00"
                endDates = "2022-07-21 17:10:00"
                # startDates = time_module(stamp)
                # endDates = time_module(stamp + 1200)
                # stamp += 1201
                not_actually_arrived(startDates, endDates)
                data_wash(waybillNo_List)
                # send_Requests(authtoken,"./有发未到模板.xlsx")
                print("ALL DONE ! Next operation coming soon......")
                time.sleep(1200)
        elif in_put == "2":
            fetch_wrong()
            # wrong_dispatch()
            pass
        elif in_put == "3":
            vehicle_info("2022-07-23", "2022-07-24")
        elif in_put.strip() == "#":
            break
        else:
            print("请输入正确的编号！")
