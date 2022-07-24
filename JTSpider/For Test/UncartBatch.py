import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import xlsxwriter as xw
import time
import pandas as pd
from tqdm import tqdm


def pre_request(headers, shipmentNo, page):
    params = {"current": page,"size": 1000,"shipmentNo": shipmentNo,"scanNetworkCode": "502701B1"}
    temp_list = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/page',headers=headers, params=params).json()
    return temp_list["data"]["pages"]

def prep_shipmentNo_Sum():
    print('请输入任务单号：\n(输入“#”以结束！)')
    shipmentNo_Sum = []
    while 1:
        shipmentNo = input('>>>')
        if (shipmentNo.strip() == "#"):
            break
        else:
            shipmentNo_Sum.append(shipmentNo)
    return shipmentNo_Sum

# def billNo_merge(headers, shipmentNo, page):
#     params = {
#         "current": page,
#         "size": 1000,
#         "shipmentNo": shipmentNo,
#         "scanNetworkCode": "0711002"
#     }
#     response = requests.get('https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/unloading/scan/page',headers=headers, params=params).json()
#     billNo_pool_temp = pd.DataFrame(response["data"]["records"])
#     billNo_sum = pd.concat([billNo_sum, billNo_pool_temp])
#     return billNo_sum

if __name__ == '__main__':
    routename = 'brancTaskTrackSearchLoading'
    # shipmentNo_Sum = prep_shipmentNo_Sum()
    shipmentNo_Sum = [
        "ZXZB22092901451",
        "ZXZB22092901331",
    ]
    print("\n正在导出单号...\n请等待...")
    billNo_Final = pd.DataFrame()
    for shipmentNo in tqdm(shipmentNo_Sum):
        page = 1
        max_page = pre_request(headers, shipmentNo, page)+ 1
        billNo_sum = pd.DataFrame()
        for page in range(max_page):
            params = {
                "current": page,
                "size": 1000,
                "shipmentNo": shipmentNo,
                "scanNetworkCode": "502701B1"
            }
            response = requests.get(
                'https://jmsgw.jtexpress.com.cn/transportation/tmsBranchTrackingDetail/loading/scan/page',headers=headers, params=params).json()
            billNo_pool_temp = pd.DataFrame(response["data"]["records"])
            billNo_sum = pd.concat([billNo_sum, billNo_pool_temp])
        print("任务单号:",shipmentNo,"导出完毕；")
        billNo_Final = pd.concat([billNo_Final, billNo_sum])
    print("正在写入Excel；")
    billNo_Final.to_excel("7.12武汉到件.xlsx", index=False)
    print("单号导出完成！")
