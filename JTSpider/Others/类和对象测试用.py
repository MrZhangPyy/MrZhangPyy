import requests



class waybillNo:
    systemAdd = ''
    actualAdd = ''
    wrongType = ''
    scanByName = ''
    scanTime = ''
    def __init__(self,systemAdd,actualAdd,wrongType,scanByName,scanTime):
        self.systemAdd = systemAdd
        self.actualAdd = actualAdd
        self.wrongType = wrongType
        self.scanByName = scanByName
        self.scanTime = scanTime

    def get_systemAdd(self):
        data = {
            "waybillNo": self,
            "countryId": "1"
        }
        response = requests.post('https://jmsgw.jtexpress.com.cn/operatingplatform/order/getOrderDetail',
                                 headers=headers, json=data).json()
        global dic_system
        systemAdd = response['data']['details']
        systemAdd = systemAdd.get('dispatchNetworkName')
        dic_system[waybillNo] = systemAdd
        return dic_system



authtoken = '46782073e9bb4132a643a5db845ad033'
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
# waybillNo_pool = [
#     "JT3006515568416",  # 漏扫错分样例单号
#     "JT2908749763772",  # 错装车样例单号
#     "JT5128747147342"  # 正常错分样例单号
# ]
dic_system = {}
waybillNo = "JT3006515568416"
p = waybillNo(waybillNo)
get_systemAdd(waybillNo)
print(dic_system)