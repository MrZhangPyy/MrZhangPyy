import requests

headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': 'c237ccec0d804726b3c1be7a3aaaf3e5',
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

taskcodepool = [
"ZXJB22089850520",
"ZXJB22089850520",
"ZXJB22089850700",
"ZXJB22089850700",
"ZXZB22089713940",
"ZXZB22089713940",
"ZXZB22089606720",
"ZXZB22089606720",
"ZXZB22089606860",
"ZXZB22089606860",
"ZXZB22089606751",
"ZXZB22089606751",
"ZXZB22089606680",
"ZXZB22089606691",
"ZXZB22087946660",
"ZXZB22086402271",
"ZXJB22090248891",
"ZXJB22090248991",
"ZXJB22090248991",
]

for taskcode in taskcodepool:
    data = {"keywordList": [taskcode],
            "trackingTypeEnum": "TASKCODE",
            "countryId": "1"
            }

    response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/podTracking/inner/query/keywordList',
                             headers=headers, json=data).json()
    response = response['data']
    response = response[0]
    response = response.get('details')
    # print()
    dic2 = {}
    for dic in response:
        type = ''
        type = dic['scanTypeName']
        if type == "到解车扫描":
            name = dic['scanByName']
            dic2[taskcode] = name
            print(dic2)
