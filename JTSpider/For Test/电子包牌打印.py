import requests

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '261f364482f74f93b2afe5b04c8d3c8d',
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

data = {"current":1,"size":100,"startCreateTime":"2022-07-15 00:00:00","endCreateTime":"2022-07-15 23:59:59","createNetworkCode":"0711002","createTimeList":["2022-07-15 00:00:00","2022-07-15 23:59:59"],"packageNumberList":["B108289306714"],"countryId":"1"}

response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page', headers=headers, data=data)
