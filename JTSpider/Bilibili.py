import requests

headers = {
    'authority': 'api.bilibili.com',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^21^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://space.bilibili.com/826104/fans/follow',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'buvid3=68BC8E58-4FEC-F12E-0C27-437DE83902E927421infoc; i-wanna-go-back=-1; b_ut=7; b_lsid=9877D517_182039A55CA; _uuid=46996723-DBCD-24FB-8366-CAB1171F98F422420infoc; buvid4=635C637A-7F37-B4A5-69F3-8F2A25B6F1D528307-022071604-DTdRc9nh8MUg7B5cukhzig^%^3D^%^3D; CURRENT_BLACKGAP=0; sid=7yvliwbu; LIVE_BUVID=AUTO7916579178681058; fingerprint=1751c08129277f13b28e1003572a1230; buvid_fp_plain=undefined; DedeUserID=826104; DedeUserID__ckMd5=20f1c377da8d3fe2; SESSDATA=01d392c9^%^2C1673469899^%^2Cd445f*71; bili_jct=b681f9c3ff434036184fab77b604d5ff; PVID=1; buvid_fp=1751c08129277f13b28e1003572a1230; CURRENT_FNVAL=4048; rpdid=^|(k)~u~umuml0J\'uYl~mu~mlR; bp_video_offset_826104=683236126309220400; innersign=1; blackside_state=0; b_timer=^%^7B^%^22ffp^%^22^%^3A^%^7B^%^22333.1007.fp.risk_68BC8E58^%^22^%^3A^%^22182039A5C08^%^22^%^2C^%^22333.42.fp.risk_68BC8E58^%^22^%^3A^%^22182039B25A7^%^22^%^2C^%^22666.4.fp.risk_68BC8E58^%^22^%^3A^%^22182039BB481^%^22^%^2C^%^22666.5.fp.risk_68BC8E58^%^22^%^3A^%^22182039C218A^%^22^%^2C^%^22666.25.fp.risk_68BC8E58^%^22^%^3A^%^22182039C3DF3^%^22^%^2C^%^22333.880.fp.risk_68BC8E58^%^22^%^3A^%^22182039FE424^%^22^%^2C^%^22333.788.fp.risk_68BC8E58^%^22^%^3A^%^22182039FFD52^%^22^%^2C^%^22333.999.fp.risk_68BC8E58^%^22^%^3A^%^2218203A244AD^%^22^%^2C^%^22888.2421.fp.risk_68BC8E58^%^22^%^3A^%^2218203A7D723^%^22^%^7D^%^7D',
}
for page in range(1,41):
    params = (
        ('vmid', '826104'),
        ('pn', page),
        ('ps', '50'),
        ('order', 'desc'),
        ('order_type', ''),
        ('jsonp', 'jsonp'),
        ('callback', 'json'),
    )
    response = requests.get('https://api.bilibili.com/x/relation/followings', headers=headers, params=params)
    print(response.text)

