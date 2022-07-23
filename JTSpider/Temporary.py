import requests
import pandas as pd
import copy

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '6abaab0aa4a3427dbc28da53256360bb',
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

load = {"current":1,
        "size":100,
        "startDepartureTime":"2022-07-22 10:00:00",
        "endDepartureTime":"2022-07-23 10:00:00",
        "startActualDepartureTime":"2022-07-22 10:00:00",
        "endActualDepartureTime":"2022-07-23 10:00:00",
        "startCode":"0711002",
        "shipmentState":4,
        "countryId":"1"
        }
unload = {"current":1,
        "size":100,
        "startDepartureTime":"2022-07-22 10:00:00",
        "endDepartureTime":"2022-07-23 10:00:00",
        "startActualDepartureTime":"2022-07-22 10:00:00",
        "endActualDepartureTime":"2022-07-23 10:00:00",
        "endtCode":"0711002",
        "shipmentState":4,
        "countryId":"1"
        }
response1 = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page', headers=headers, json=load).json()
response1 = response1["data"]["records"]
list_ = []
for dic in response1:
    dic_new = {}
    dic_new["运输单号"] = dic["shipmentNo"]
    dic_new["始发转运"] = dic["startName"]
    dic_new["目的网点"] = dic["endName"]
    dic_new["线路方式"] = dic["startName"] + "-" + dic["endName"]
    dic_new["计划发车时间"] = dic["plannedDepartureTime"]
    dic_new["实际发车时间"] = dic["actualDepartureTime"]
    dic_new["车牌号"] = dic["plateNumber"]
    headers = {
        'authority': 'jmsgw.jtexpress.com.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authtoken': '6abaab0aa4a3427dbc28da53256360bb',
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
    params = (('shipmentNo', dic["shipmentNo"]),)
    response2 = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list',
                            headers=headers, params=params).json()
    dic_new["装载票数"] = response2["data"][0]["scanWaybillNum"]
    dic_new["车型"] = dic["actualVehicleTypegroup"]
    list_.append(copy.deepcopy(dic_new))
print(list_)
