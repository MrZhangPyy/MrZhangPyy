routename = 'electronicPackagePrinting'
    headers_generator(routename)
    data = {"current": 1, "size": 20, "startCreateTime": "2022-07-15 00:00:00", "endCreateTime": "2022-07-15 23:59:59",
            "createNetworkCode": "0711002", "packageNumberList": packageNum_list, "countryId": "1"}
    response = requests.post('https://jmsgw.jtexpress.com.cn/customerother/electronicpackagelist/page',
                             headers=headers, json=data).json()
    response = response['data']['records']
    for dic in tqdm(response):
        if dic.get('packageCode') == "501" and (dic.get('createNetworkCode') == "502701B1" or dic.get('createNetworkCode') == "502701"):
            pass
        elif
        else:packageNum_list.remove(dic.get('packageNumber'))
    print(packageNum_list)