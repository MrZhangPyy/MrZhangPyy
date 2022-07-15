import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import xlsxwriter as xw
import time


def exportToExcel(title, dataList, start):
    for item in dataList:
        row = [item[title[0]], item[title[1]], item[title[2]], item[title[3]], item[title[4]], item[title[5]],
               item[title[6]], item[title[7]], item[title[8]], item[title[9]], item[title[10]], item[title[11]],
               item[title[12]], item[title[13]]]
        worksheet.write_row('A' + str(start), row)
        start = start + 1


def request_data(resultDatas, headers, page, pageSize, startTime, endTime):
    data = {"current": page,
            "size": pageSize,
            "startDates": startTime,
            "endDates": endTime,
            "scanSite": "0711002",
            "scanType": "发件扫描",
            "filterNo": "2",
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
    requestStartTime = time.time()
    temp_list = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                              headers=headers, json=data).json()
    requestEndTime = time.time()
    print("请求", page, "结束, 耗时：", requestEndTime - requestStartTime, "秒！")

    # if len(temp_list["data"]["records"]) == 0:
    #     break
    exportStartTime = time.time()
    # exportToExcel(title, temp_list["data"]["records"], startRow + (page - 1) * 1000)
    exportEndTime = time.time()
    print("查询", page, "结束, 耗时：", exportEndTime - exportStartTime, "秒！")
    resultDatas.extend(temp_list["data"]["records"])
    return page


def first_request(headers, page, pageSize, startTime, endTime):
    data = {"current": page,
            "size": pageSize,
            "startDates": startTime,
            "endDates": endTime,
            "scanSite": "0711002",
            "scanType": "发件扫描",
            "filterNo": "2",
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
    requestStartTime = time.time()
    temp_list = requests.post('https://jmsgw.jtexpress.com.cn/bigdataoperatingplatform/scanRecordQuery/listPage',
                              headers=headers, json=data).json()
    requestEndTime = time.time()
    print("首次页数请求", page, "结束, 耗时：", requestEndTime - requestStartTime, "秒！")
    return temp_list["data"]["total"]


def get_date():
    print("请输入日期：(例：2022-05-26）\n")
    date = input('>>>')
    return date


if __name__ == '__main__':
    dayTime = get_date()
    headers = {
        'authority': 'jmsgw.jtexpress.com.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authtoken': '922fd1fb1a23478a8a64f1819270dcfb',
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

    start_time = time.time()
    page = 1

    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix="export_")

    # 导出地址
    workbook = xw.Workbook('/Users/Administrator/OneDrive - 极兔速递/桌面/JSPYDER/Output1.xlsx')  # 创建工作簿
    worksheet = workbook.add_worksheet("1")  # 创建子表
    worksheet.activate()  # 激活表
    i = 2  # 从第二行开始写入数据
    title = ['billNo', 'belongNo', 'scanType', 'scanDate', 'inputDept',
             'upOrNextStation', 'weight', 'sendSite', 'scanEmp', 'employeeCode',
             'baGunId', 'bulkWeight', 'terminalDispatchCode', 'destinationNetworkName']  # 设置表头
    worksheet.write_row('A1', title)  # 从A1单元格开始写入表头
    total = 0
    subTotal = 0
    # 分开一天的时间
    # dayTime = "2022-05-26"
    times = [{"startTime": " 00:00:00", "endTime": " 02:00:00"},
             {"startTime": " 02:00:01", "endTime": " 04:00:00"},
             {"startTime": " 04:00:01", "endTime": " 06:00:00"},
             {"startTime": " 06:00:01", "endTime": " 08:00:00"},
             {"startTime": " 08:00:01", "endTime": " 10:00:00"},
             {"startTime": " 10:00:01", "endTime": " 12:00:00"},
             {"startTime": " 12:00:01", "endTime": " 14:00:00"},
             {"startTime": " 14:00:01", "endTime": " 16:00:00"},
             {"startTime": " 16:00:01", "endTime": " 18:00:00"},
             {"startTime": " 18:00:01", "endTime": " 20:00:00"},
             {"startTime": " 20:00:01", "endTime": " 22:00:00"},
             {"startTime": " 22:00:01", "endTime": " 23:59:59"}]
    startRow = 2
    for item in times:
        startTime = dayTime + item.get("startTime")
        endTime = dayTime + item.get("endTime")
        # 首先确定时间范围内的条数及总页数
        subTotal = first_request(headers, 1, 100, startTime, endTime)

        print("子时间总数：" + str(subTotal))
        pageSize = 1000
        max_page = int(subTotal / pageSize + 2)
        obj_list = []
        resultDatas = []
        for page in range(max_page):
            obj = threadPool.submit(request_data, resultDatas, headers, page, pageSize, startTime, endTime)
            obj_list.append(obj)

        total = subTotal + total

        for future in as_completed(obj_list):
            data = future.result()
            print(f"done: {len(resultDatas)}")

        exportToExcel(title, resultDatas, startRow)
        startRow = startRow + len(resultDatas)
        print(f"本次时间已全部导出，行数： {len(resultDatas)}")

    end_time = time.time()
    total_time_cost = end_time - start_time
    print("程序结束, ", total, "行数据已保存，总计耗时：", total_time_cost, "秒！")
    workbook.close()  # 关闭表
    threadPool.shutdown(wait=True)
