import requests
import pandas as pd

waybillNo_Pool = pd.DataFrame([{"运单号":"JT3008040951422","包号":"B112221940572"},{"运单号":"JT5133085578150","包号":"B112307355581"}])
print(waybillNo_Pool)
packageNum_List = ['B112221940572', 'B112307355581']
data = {"current":1,"size":1000,"startCreateTime":"2022-07-15 00:00:00","endCreateTime":"2022-07-15 23:59:59",
         "createNetworkCode":"0711002","packageNumberList":packageNum_List,"countryId":"1"}
headers = {
        'authority': 'jmsgw.jtexpress.com.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authtoken': '93983eaf46a34ee49d85132398109ee4',
        'cache-control': 'max-age=2, must-revalidate',
        'content-type': 'application/json;charset=UTF-8',
        'lang': 'zh_CN',
        'origin': 'https://jms.jtexpress.com.cn',
        'referer': 'https://jms.jtexpress.com.cn/',
        'routename': 'electronicPackagePrinting',
        'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                                 headers=headers,json=data).json()
response = response['data']['records']
print(packageNum_List)
print(response)
for dic in response:
    if dic.get('packageCode') == "501" and (dic.get('createNetworkCode') == "502701B1" or dic.get('createNetworkCode') == "502701"):
        pass
    else:packageNum_List.remove(dic.get('packageNumber'))
print(packageNum_List)
waybillNo_Pool = waybillNo_Pool[waybillNo_Pool["包号"].isin(packageNum_List)]
print(waybillNo_Pool)
