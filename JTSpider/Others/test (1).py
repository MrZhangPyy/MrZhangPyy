import requests
import pandas as pd

# import json

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '4e90f2041a2d489a8f15492d02b66e48',
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
data = {"current": page,
        "size": 200,
        "startDates": "2022-05-12 00:00:00",
        "endDates": "2022-05-12 00:10:00",
        "scanSite": "0711002",
        "scanType": "发件扫描",
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

response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage', headers=headers, json=data).json()
billcount = response["data"]["total"]
maxpage = response["data"]["pages"]
numpool = response["data"]["records"]
for page in range(maxpage):
    for i in range(len(numpool)):
        for k, v in numpool[i].items():
            print(k, v)
        print("*" * 50)
page = page + 1

print("操作量：", billcount)

# data = {
#     "current": 1,
#     "size": 20,
#     "startDate": "2022-05-12",
#     "endDate": "2022-05-12",
#     "dateType": "1",
#     "queryType": 2,
#     "entrepotCode1": "0711002",
#     "hasSourceList": 0,
#     "countryId": "1"
#         }
#
# response = requests.post('https://jmsgw.jtexpress.com.cn/businessindicator/bigdataReport/detailDir/businessin/operate/entrepot_monitor_new_count', headers=headers, json=data).json()
# print(response["data"]["records"])


# {
# "scanTypeCode":"01",
# "scanTypeName":"无头件登记",
# "scanNetworkCode":"0711002",
# "scanNetworkName":"鄂州葛店集散点",
# "scanSource":4,
# "itemType":"bm000003",
# "itemName":"毛绒玩具收纳桶",
# "commodityBrand":"无",
# "isComplete":2,
# "goodsNumber":"1",
# "weight":"0.83",
# "size":4410,
# "inspectDepartment":"",
# "residueWaybillNo":"",
# "findLinks":"2",
# "taskListNo":"",
# "findTime":"",
# "lastNetworkName":"",
# "remark":"毛绒玩具收纳桶卡扣款双膜900ⅹ1500MM一个 实际重量为0.83kg 7.90.7",
# "imgs":"ylfile/problemPiece/414b56e590fd41d7963e6dd875916f96.jpg,ylfile/problemPiece/fb4aa862f1ff49a98cf9b0a4cf581e82.jpg,ylfile/problemPiece/e5a87e469a3e4cb1baec8e629066c409.jpg,ylfile/problemPiece/71b8c9f6854149358420bb9b67473325.jpg,ylfile/problemPiece/b234bbbae3564f49a5e9b7bd4158769e.jpg,ylfile/problemPiece/2448774d8a024304b9baf3fc6153a6b6.jpg",
# "length":"7",
# "width":"90",
# "height":"7",
# "itemTypeName":"生活用品",
# "countryId":"1"
# }