import requests

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': 'c973b73408694e379b97f396fdf37302',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'routename': 'issuedButNotReceivedAlert',
    'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

data = {"current":1,"size":1000,"startTime":"2022-07-21","endTime":"2022-07-21","countryId":"1"}

response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/sendWarning/listPage', headers=headers, json=data).json()
response = response["data"]["records"]
print(response)
