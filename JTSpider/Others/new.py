import requests

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '2d19a6d62c9e43e19a82164b95b3295d',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'branchTaskNew',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
}

data = {
    "current": 1,
    "size": 100,
    "startCode": "0711002",
    "endCode": "502701",
    "startDepartureTime": "2022-06-11 00:00:00",
    "endDepartureTime": "2022-06-11 23:59:59",
    "channel": "taskManagement",
    "countryId": "1"
}

response = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsnewBranchShipment/page', headers=headers, json=data)
