import pandas as pd
import requests


headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '0bde4a1f3f9b4b328d0b8d83a19e5760',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'arriveAndSendLeakage',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

data = {"current":1,
        "size":1000,
        "startDate":"2022-07-02 00:00:00",
        "endDate":"2022-07-02 23:59:59",
        "regionCode":"200001",
        "proxyAreaCode":"420000",
        "siteCode":"0711002",
        "queryType":2,
        "condition3":[3,4],
        "countryId":"1"}

response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/transferlackscan/listDetail', headers=headers, json=data).json()
bill_no_pool = response["data"]["records"]
df = pd.DataFrame(bill_no_pool)
df.to_excel("test2.xlsx", index=False)
