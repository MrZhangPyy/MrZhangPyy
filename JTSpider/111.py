import requests

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

params = (('shipmentNo', 'ZXJB22097668440'),)

response = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/list', headers=headers, params=params).json()
print(response["data"][0]["scanWaybillNum"])
