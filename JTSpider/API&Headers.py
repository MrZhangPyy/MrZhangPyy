authtoken = ''
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
        'routename': routename,
        'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

# 接口1：https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/arriveMonitor/listDetail
# 接口1 routename = 'newArriveMonitor'
# 接口1 payload = {"current":1,"size":20,"startDates":"2022-07-13 00:00:00","endDates":"2022-07-13 23:59:59","siteCode":"0711002","exportType":6,"type":6,"countryId":"1"}

# 接口2：https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage
# 接口2 routename = 'scanQueryConstantlyNew'
# 接口2 payload = {"current":1,"size":200,"startDates":"2022-07-13 00:00:00","endDates":"2022-07-13 23:59:59","scanType":"全部","sortName":"scanDate","sortOrder":"desc","bilNos":["第一步的结果list"],"queryTerminalDispatchCode":0,"querySub":"","reachAddressCodeList":[],"sendSites":[],"billType":1,"countryId":"1"}

# 接口3：https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/import
# 接口3 routename = 'batchProblem'
# 接口3 payload：

# ------WebKitFormBoundaryoOwRvCGxHAG1pgYr
# Content-Disposition: form-data; name="uploadFile"; filename="有发未到模板.xlsx"
# Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
#
#
# ------WebKitFormBoundaryoOwRvCGxHAG1pgYr--