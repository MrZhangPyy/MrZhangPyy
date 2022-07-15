import requests
import pandas as pd
from time import *
from threading import Thread
from queue import Queue


headers = {
    'authority': 'jmsgw.jtexpress.com.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authtoken': '0447eefec45c4c7c90964f52a8a04500',
    'cache-control': 'max-age=2, must-revalidate',
    'content-type': 'application/json;charset=UTF-8',
    'lang': 'zh_CN',
    'origin': 'https://jms.jtexpress.com.cn',
    'referer': 'https://jms.jtexpress.com.cn/',
    'routename': 'scanQueryConstantlyNew',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}
# 定义headers


page = 1
# 设定初始页数


pre_pay_load = {"current": page,#当前页面
        "size": 1000,#单页数据行数
        "startDates": "2022-05-13 10:00:00",#开始时间
        "endDates": "2022-05-13 12:00:00",#结束时间
        "scanSite": "0711002",#扫描网点编号，无需更改
        "scanType": "发件扫描",#扫描类型，根据需要更改
        "filterNo": "2", #注释掉此行则查询全部，否则为只查询单号
        "sortName": "scanDate",
        "sortOrder": "desc",
        "bilNos": [],
        "queryTerminalDispatchCode": 0,
        "querySub": "",
        "reachAddressList": [],
        "sendSites": [],
        "billType": 1,
        "countryId": "1"
        }
#payload定义结束


begin_time = time()
raw_res = requests.post(
        'https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
        headers=headers,
        json=pre_pay_load
    ).json()
bill_count = raw_res["data"]["total"]
#总行数
max_page = raw_res["data"]["pages"]
#总页数
df_result = {}
# 载入空数据帧用于存储数据
for page in range(max_page):
    data = {"current": page,  # 当前页面
                "size": 1000,  # 单页数据行数
                "startDates": "2022-05-13 10:00:00",  # 开始时间
                "endDates": "2022-05-13 12:00:00",  # 结束时间
                "scanSite": "0711002",  # 扫描网点编号，无需更改
                "scanType": "发件扫描",  # 扫描类型，根据需要更改
                "filterNo": "2",  # 注释掉此行则查询全部，否则为只查询单号
                "sortName": "scanDate",
                "sortOrder": "desc",
                "bilNos": [],
                "queryTerminalDispatchCode": 0,
                "querySub": "",
                "reachAddressList": [],
                "sendSites": [],
                "billType": 1,
                "countryId": "1"
            }
    #payload定义结束
    response = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',headers=headers,json=data).json()# 获取数据所处列表
    bill_no_pool = response["data"]["records"]
    df = pd.DataFrame(bill_no_pool)
    df = df[['billNo', 'belongNo', 'scanType', 'scanDate', 'inputDept', 'upOrNextStation', 'weight', 'sendSite', 'scanEmp', 'employeeCode', 'baGunId', 'bulkWeight', 'terminalDispatchCode', 'destinationNetworkName']]
    print(df)
    page = page + 1
    # df_result = pd.concat([df_result, df])#合并数据帧


# data_gathering_ended_time = time()
# gathering_time_cost = data_gathering_ended_time - begin_time
# print("数据读取完毕，耗时", gathering_time_cost, "秒。")
#
#
# df_result.to_excel("test.xlsx", index=False)
# data_saving_ended_time = time()
# saving_time_cost = data_saving_ended_time - data_gathering_ended_time
# print("数据写入完毕，耗时", saving_time_cost, "秒。")
#
#
# total_time_cost = data_saving_ended_time - begin_time
# print("程序结束，", bill_count, "行数据已保存，总计耗时：", total_time_cost, "秒！")
