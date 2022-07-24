import requests
from tqdm import tqdm



billNo_pool = []
authtoken = 'c237ccec0d804726b3c1be7a3aaaf3e5'
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
    'routename': 'trackingExpress',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

for waybillNo in tqdm(billNo_pool):
    data = {"keywordList": [waybillNo],
            "trackingTypeEnum": "WAYBILL",
            "countryId": "1"
            }
    response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/podTracking/inner/query/keywordList',
                             headers=headers,json=data).json()
    response = response["data"][0]['details']
    for dic in tqdm(response):
        temp1 = ''
        temp2 = ''
        temp1 = dic['scanNetworkName']
        temp2 = dic['scanTypeName']
        if temp1 == "鄂州葛店集散点":
            if temp2 == "集货到件":
                temp3 = 2
                temp3 = response.index(dic)
                temp3 = temp3 -1
        result = ''
        result = response[temp3]
        result = result['scanNetworkName']
        print(waybillNo, result)

