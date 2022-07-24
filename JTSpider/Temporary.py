import requests
import pandas as pd
import copy
from tqdm import tqdm

authtoken = 'f96135b8a2d643ae8da327a4c925c192'
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
    'routename': 'brancTaskTrackSearch',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
headers2 = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': authtoken,
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=utf-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'brancTaskTrackSearchView',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
headers3 = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': authtoken,
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=utf-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'monitoringSearch',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
headers4 = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': authtoken,
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=utf-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'monitoringSearchView',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
load = {"current": 1,
        "size": 100,
        "startDepartureTime": "2022-07-23 10:00:00",
        "endDepartureTime": "2022-07-24 10:00:00",
        "startActualDepartureTime": "2022-07-23 10:00:00",
        "endActualDepartureTime": "2022-07-24 10:00:00",
        "startCode": "0711002",
        "shipmentState": 4,
        "countryId": "1"
        }
unload = {"current": 1,
          "size": 100,
          "startDepartureTime": "2022-07-23 10:00:00",
          "endDepartureTime": "2022-07-24 10:00:00",
          "startActualDepartureTime": "2022-07-23 10:00:00",
          "endActualDepartureTime": "2022-07-24 10:00:00",
          "endCode": "0711002",
          "shipmentState": 4,
          "countryId": "1"
          }

response1 = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page', headers=headers,
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
    response2 = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list',
                             headers=headers2, params=params).json()
    dic_new["装载票数"] = response2["data"][0]["scanWaybillNum"]
    dic_new["车型"] = dic["actualVehicleTypegroup"]
    list_.append(copy.deepcopy(dic_new))

response3 = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page', headers=headers,
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
    response4 = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list',
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
