import requests

headers = {
    'authority': 'api.maplestory.gg',
    'sec-ch-ua': '^\\^Google',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'origin': 'https://maplestory.gg',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://maplestory.gg/',
    'accept-language': 'zh-CN,zh;q=0.9',
}

print(requests.get('https://api.maplestory.gg/v2/public/character/gms/Wweixiao', headers=headers).text)