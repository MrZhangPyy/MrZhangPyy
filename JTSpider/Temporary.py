import requests
import pandas as pd

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

data = {"current":1,
        "size":100,
        "startDepartureTime":"2022-07-22 10:00:00",
        "endDepartureTime":"2022-07-23 10:00:00",
        "startActualDepartureTime":"2022-07-22 10:00:00",
        "endActualDepartureTime":"2022-07-23 10:00:00",
        "startCode":"0711002",
        "shipmentState":4,
        "countryId":"1"
        }
data2 = {"current":1,
        "size":100,
        "startDepartureTime":"2022-07-22 10:00:00",
        "endDepartureTime":"2022-07-23 10:00:00",
        "startActualDepartureTime":"2022-07-22 10:00:00",
        "endActualDepartureTime":"2022-07-23 10:00:00",
        "endtCode":"0711002",
        "shipmentState":4,
        "countryId":"1"
        }
response = requests.post('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/page', headers=headers, json=data).json()
response = response["data"]["records"]
response = pd.DataFrame(response)
response.to_excel("test.xlsx",index=False)