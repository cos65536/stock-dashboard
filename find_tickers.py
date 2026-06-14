import requests
import json
import urllib.parse

names = [
    "TIGER 미국필라델피아반도체나스닥",
    "ACE 글로벌반도체TOP4",
    "KODEX 미국반도체",
    "TIGER 미국필라델피아AI반도체나스닥",
    "KODEX 미국AI전력핵심인프라",
    "TIGER 글로벌AI전력인프라",
    "KODEX 미국AI광통신네트워크",
    "KODEX 미국우주항공",
    "SOL 미국테크TOP10",
    "TIGER 미국테크TOP10",
    "ACE 미국빅테크TOP7",
    "ACE 미국나스닥100",
    "ACE 미국S&P500",
    "SOL 미국배당다우존스",
    "ACE 미국배당다우존스",
    "RISE 200",
    "PLUS 고배당주",
    "TIGER 은행고배당플러스"
]

for name in names:
    url = f"https://ac.finance.naver.com/ac?q={urllib.parse.quote(name)}&st=111&r_lt=111"
    try:
        res = requests.get(url)
        data = res.json()
        items = data.get('items', [])
        if items and items[0]:
            code = items[0][0][0]
            fullname = items[0][0][1]
            print(f"'{code}.KS': ('{fullname}', '{name}'),")
        else:
            print(f"# Not found: {name}")
    except Exception as e:
        print(f"Error for {name}: {e}")
