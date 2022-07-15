import requests
from tqdm import tqdm



billNo_pool = [
"JT5129687789493",
"JT5129573839980",
"JT3006817700720",
"JT3006859210034",
"JT3006856040717",
"JT3006847009651",
"JT3006776038105",
"JT3006825678605",
"JT5129967292206",
"JT3006826117128",
"JT5129969240642",
"JT5129854842243",
"JT5129855028917",
"JT5129973058401",
"JT3006823034794",
"JT3006796301007",
"JT5129803412927",
"JT5129828544280",
"JT3006803044563",
"JT2908940177335",
"JT5129975626929",
"JT5129975393619",
"JT5129783838324",
"JT5129700222872",
"JT5129712409552",
"JT3006819581325",
"JT2908932244651",
"JT2908909541976",
"JT5129784139675",
"JT5129783805549",
"JT2908913790414",
"JT5129784140161",
"JT5129778495105",
"JT5129717262096",
"JT5129784133859",
"JT5129734364857",
"JT5129784107815",
"JT5129783841065",
"JT5129784107020",
"JT5129784137986",
"JT2908921166714",
"JT5129791160183",
"JT5129784138296",
"JT5129527849310",
"JT5129798412653",
"JT2908908974873",
"JT3006846356912",
"JT2908909353954",
"JT2908911072332",
"JT5129723095063",
"JT5129691528871",
"JT3006863500026",
"JT3003075506173",
"JT2908911072343",
"JT5129741424891",
"JT5129830764034",
"JT5129570848146",
"JT5129699058602",
"JT2908911072309",
"JT2908910483497",
"JT2908908106548",
"JT2908911072423",
"JT5129802860375",
"JT5129707342802",
"JT5129708015120",
"JT0005896308003",
"JT3006877844541",
"JT3006823028670",
"JT5129708300225",
"JT5129563882802",
"JT5129708017922",
"JT3006837475760",
"JT3006804363879",
"JT2908919372696",
"JT5129704944238",
"JT2908922761393",
"JT5129691848111",
"JT5129780630543",
"JT5129742378463",
"JT3006827149238",
"JT5129725186613",
"JT2908909619145",
"JT5129838571199",
"JT5129815550746",
"JT5129689915833",
"JT5129848403532",
"JT3006796729038",
"JT5129573840283",
"JT5129830360296",
"JT5129813850566",
"JT5129849999279",
"JT5129847803566",
"JT5129830360796",
"JT5128969778729",
"JT5129842658580",
"JT5129816111026",
"JT5129814028367",
"JT5129718120619",
"JT5129547118184",
"JT2908933942592",
"JT5129593604683"
]
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

