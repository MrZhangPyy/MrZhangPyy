import requests


def get_info(waybillNo):
    data = {
                "waybillNo": waybillNo,
                "defaultReceiver": 3,
                "defaultKnow": 2,
                "countryId": "1"
                }
    response = requests.post('https://jmsgw.jtexpress.com.cn/sqsthird/comboBox/queryReceiverAndKnowNetwork', headers=headers, json=data).json()
    # receiverNetwork = response['data']['receiverNetwork']['id']
    # knowNetwork = str(response['data']['knowNetwork']['id'])
    return response


def send_msg(waybillNo, receiverNetwork, knowNetwork):
    data = {
        "waybillNo": waybillNo,
        "replyContent": "",
        "problemPieceId": "",
        "probleTypeSubjectId": 121,
        "probleTypeSubjectId2": 100039,
        "receiveNetworkId": receiverNetwork,
        "replyContentImg": [],
        "replyStatus": 0,
        "probleTypeId": 2,
        "probleDescription": "此件显示发往我司，但实际并未到达！",
        "uploadDataProp": "",
        "knowNetwork": knowNetwork,
        "defaultKnow": 2,
        "firstLevelTypeName": "有发未到件",
        "problemTypeSubjectCode": "29",
        "secondLevelTypeId": 100039,
        "secondLevelTypeCode": "29a",
        "secondLevelTypeName": "有发未到件a",
        "paths": "",
        "countryId": "1"
    }

    sub_response = requests.post('https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/registration',
                                 headers=headers, json=data)
    print(waybillNo, "接收网点：", receiverNetwork, "知悉网点：", knowNetwork, "已完成...还剩余", lenth, "条；")


if __name__ == '__main__':
    headers = {
                'authority': 'jmsgw.jtexpress.com.cn',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'authtoken': '1a17b75b6ed14645b6cffd24a433da47',
                'cache-control': 'max-age=2, must-revalidate',
                'content-type': 'application/json;charset=UTF-8',
                'lang': 'zh_CN',
                'origin': 'https://jms.jtexpress.com.cn',
                'referer': 'https://jms.jtexpress.com.cn/',
                'routename': 'batchProblem',
                'sec-ch-ua': '^\\^',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '^\\^Windows^\\^',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                }
    billNo = []
    lenth = len(billNo) - 1
    succ_count = 0
    fail_count = 0
    for waybillNo in billNo:
        # get_info(waybillNo)
        data = {
            "waybillNo": waybillNo,
            "defaultReceiver": 3,
            "defaultKnow": 2,
            "countryId": "1"
        }
        response = requests.post('https://jmsgw.jtexpress.com.cn/sqsthird/comboBox/queryReceiverAndKnowNetwork',
                                 headers=headers, json=data).json()
        receiverNetwork = response['data']['receiverNetwork']['id']
        knowNetwork = str(response['data']['knowNetwork']['id'])
        data = {
            "waybillNo": waybillNo,
            "replyContent": "",
            "problemPieceId": "",
            "probleTypeSubjectId": 121,
            "probleTypeSubjectId2": 100039,
            "receiveNetworkId": receiverNetwork,
            "replyContentImg": [],
            "replyStatus": 0,
            "probleTypeId": 2,
            "probleDescription": "此件显示发往我司，但实际并未到达！",
            "uploadDataProp": "",
            "knowNetwork": knowNetwork,
            "defaultKnow": 2,
            "firstLevelTypeName": "有发未到件",
            "problemTypeSubjectCode": "29",
            "secondLevelTypeId": 100039,
            "secondLevelTypeCode": "29a",
            "secondLevelTypeName": "有发未到件a",
            "paths": "",
            "countryId": "1"
        }

        sub_response = requests.post('https://jmsgw.jtexpress.com.cn/servicequality/problemPiece/registration',
                                     headers=headers, json=data).json()
        msg = sub_response.get('msg')
        while msg == '请求成功':
            succ_count = succ_count + 1
            break
        while msg == '轨迹显示快件已到，请重新确认':
            fail_count = fail_count + 1
            break
        while msg == '运单已签收，不允许问题件录入':
            fail_count = fail_count + 1
            break
        print(waybillNo, "接收网点：", receiverNetwork, "知悉网点：", knowNetwork, msg, "——————还剩余", lenth, "条；")
        lenth = lenth -1
    print("今日批量有发未到已完成！成功%d条，失败%d条！" % (succ_count, fail_count))
