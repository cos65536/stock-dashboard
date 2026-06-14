import re

us_stocks = {
    'AAPL': ('Apple', '애플'), 'MSFT': ('Microsoft', '마이크로소프트'), 'GOOGL': ('Alphabet', '구글'),
    'AMZN': ('Amazon', '아마존'), 'NVDA': ('NVIDIA', '엔비디아'), 'META': ('Meta', '메타'),
    'TSLA': ('Tesla', '테슬라'), 'TSM': ('TSMC', 'TSMC'), 'AVGO': ('Broadcom', '브로드컴'),
    'LLY': ('Eli Lilly', '일라이 릴리'), 'JPM': ('JPMorgan Chase', 'JP모건'), 'V': ('Visa', '비자'),
    'WMT': ('Walmart', '월마트'), 'NFLX': ('Netflix', '넷플릭스'), 'AMD': ('AMD', 'AMD'),
    'BRK-B': ('Berkshire Hathaway', '버크셔 해서웨이'), 'XOM': ('Exxon Mobil', '엑슨 모빌'),
    'JNJ': ('Johnson & Johnson', '존슨앤드존슨'), 'PLTR': ('Palantir', '팔란티어'), 'QCOM': ('Qualcomm', '퀄컴'),
    'COST': ('Costco', '코스트코'), 'DIS': ('Walt Disney', '디즈니'), 'CRM': ('Salesforce', '세일즈포스'),
    'PG': ('Procter & Gamble', 'P&G'), 'MA': ('Mastercard', '마스터카드'), 'HD': ('Home Depot', '홈디포'),
    'BAC': ('Bank of America', '뱅크오브아메리카'), 'ABBV': ('AbbVie', '애브비'), 'CVX': ('Chevron', '쉐브론'),
    'KO': ('Coca-Cola', '코카콜라'), 'PEP': ('PepsiCo', '펩시코'), 'MRK': ('Merck', '머크'),
    'TMO': ('Thermo Fisher', '써모피셔'), 'ADBE': ('Adobe', '어도비'), 'MCD': ('McDonalds', '맥도날드'),
    'CSCO': ('Cisco', '시스코'), 'ACN': ('Accenture', '액센츄어'), 'ABT': ('Abbott Labs', '애벗 연구소'),
    'LIN': ('Linde', '린데'), 'DHR': ('Danaher', '다나허'), 'TXN': ('Texas Instruments', '텍사스 인스트루먼트'),
    'NEE': ('NextEra Energy', '넥스테라 에너지'), 'PFE': ('Pfizer', '화이자'), 'PM': ('Philip Morris', '필립 모리스'),
    'WFC': ('Wells Fargo', '웰스파고'), 'COP': ('ConocoPhillips', '코노코필립스'), 'UNP': ('Union Pacific', '유니온 퍼시픽'),
    'HON': ('Honeywell', '허니웰'), 'RTX': ('Raytheon', '레이시온'), 'INTC': ('Intel', '인텔'),
    'BA': ('Boeing', '보잉'), 'IBM': ('IBM', 'IBM'), 'GE': ('General Electric', 'GE'),
    'AMGN': ('Amgen', '암젠'), 'NOW': ('ServiceNow', '서비스나우'), 'SPGI': ('S&P Global', 'S&P 글로벌'),
    'CAT': ('Caterpillar', '캐터필라'), 'C': ('Citigroup', '씨티그룹'), 'GS': ('Goldman Sachs', '골드만삭스'),
    'INTU': ('Intuit', '인튜이트'), 'BKNG': ('Booking Holdings', '부킹 홀딩스'), 'UNH': ('UnitedHealth', '유나이티드헬스'),
    'ISRG': ('Intuitive Surgical', '인튜이티브 서지컬'), 'SYK': ('Stryker', '스트라이커'), 'TJX': ('TJX Companies', 'TJX'),
    'PGR': ('Progressive', '프로그레시브'), 'BSX': ('Boston Scientific', '보스턴 사이언티픽'), 'REGN': ('Regeneron', '리제네론'),
    'CB': ('Chubb', '처브'), 'MDT': ('Medtronic', '메드트로닉'), 'MMC': ('Marsh & McLennan', '마쉬앤맥레넌'),
    'MU': ('Micron Technology', '마이크론'), 'SO': ('Southern Co', '서던 컴퍼니'), 'ADP': ('Automatic Data', 'ADP'),
    'FI': ('Fiserv', '파이서브'), 'BDX': ('Becton Dickinson', '벡톤 디킨슨'), 'ICE': ('Intercontinental Exchange', 'ICE'),
    'CME': ('CME Group', 'CME 그룹'), 'WM': ('Waste Management', '웨이스트 매니지먼트'), 'AON': ('Aon', '에이온'),
    'CL': ('Colgate-Palmolive', '콜게이트'), 'EOG': ('EOG Resources', 'EOG 리소스'), 'ITW': ('Illinois Tool', '일리노이 툴'),
    'SLB': ('Schlumberger', '슐럼버거'), 'T': ('AT&T', 'AT&T'), 'VZ': ('Verizon', '버라이즌'),
    'F': ('Ford', '포드'), 'GM': ('General Motors', 'GM'), 'KHC': ('Kraft Heinz', '크래프트 하인즈'),
    'UBER': ('Uber', '우버'), 'ABNB': ('Airbnb', '에어비앤비'), 'SNOW': ('Snowflake', '스노우플레이크'),
    'SHOP': ('Shopify', '쇼피파이'), 'SQ': ('Block', '블록'), 'PYPL': ('PayPal', '페이팔'),
    'COIN': ('Coinbase', '코인베이스'), 'HOOD': ('Robinhood', '로빈후드'), 'ZM': ('Zoom', '줌'),
    'RBLX': ('Roblox', '로블록스'), 'U': ('Unity', '유니티')
}

kr_stocks = {
    '005930.KS': ('Samsung Electronics', '삼성전자'), '000660.KS': ('SK Hynix', 'SK하이닉스'),
    '373220.KS': ('LG Energy Solution', 'LG에너지솔루션'), '207940.KS': ('Samsung Biologics', '삼성바이오로직스'),
    '005380.KS': ('Hyundai Motor', '현대차'), '000270.KS': ('Kia', '기아'),
    '068270.KS': ('Celltrion', '셀트리온'), '035420.KS': ('NAVER', '네이버'),
    '035720.KS': ('Kakao', '카카오'), '051910.KS': ('LG Chem', 'LG화학'),
    '005490.KS': ('POSCO', 'POSCO홀딩스'), '105560.KS': ('KB Financial', 'KB금융'),
    '055550.KS': ('Shinhan Fin', '신한지주'), '015760.KS': ('KEPCO', '한국전력'),
    '012330.KS': ('Hyundai Mobis', '현대모비스'), '066570.KS': ('LG Electronics', 'LG전자'),
    '028260.KS': ('Samsung C&T', '삼성물산'), '033780.KS': ('KT&G', 'KT&G'),
    '051900.KS': ('LG H&H', 'LG생활건강'), '034730.KS': ('SK', 'SK'),
    '032830.KS': ('Samsung Life', '삼성생명'), '011200.KS': ('HMM', 'HMM'),
    '018260.KS': ('Samsung SDS', '삼성SDS'), '096770.KS': ('SK Innovation', 'SK이노베이션'),
    '010950.KS': ('S-Oil', 'S-Oil'), '003550.KS': ('LG Corp', 'LG'),
    '323410.KS': ('Kakao Bank', '카카오뱅크'), '316140.KS': ('Woori Fin', '우리금융지주'),
    '024110.KS': ('IBK', '기업은행'), '377300.KS': ('Kakao Pay', '카카오페이'),
    '259960.KS': ('Krafton', '크래프톤'), '011170.KS': ('Lotte Chem', '롯데케미칼'),
    '009150.KS': ('Samsung Electro-Mech', '삼성전기'), '004020.KS': ('Hyundai Steel', '현대제철'),
    '042660.KS': ('Hanwha Ocean', '한화오션'), '010130.KS': ('Korea Zinc', '고려아연'),
    '005830.KS': ('DB Insurance', 'DB손해보험'), '011070.KS': ('LG Innotek', 'LG이노텍'),
    '090430.KS': ('Amorepacific', '아모레퍼시픽'), '036570.KS': ('NCSoft', '엔씨소프트'),
    '021240.KS': ('Coway', '코웨이'), '086280.KS': ('Hyundai Glovis', '현대글로비스'),
    '078930.KS': ('Yuhan', '유한양행'), '029780.KS': ('Samsung Card', '삼성카드'),
    '271560.KS': ('Orion', '오리온'), '010140.KS': ('Samsung Heavy', '삼성중공업'),
    '028050.KS': ('Hanwha Aerospace', '한화에어로스페이스'), '006400.KS': ('Samsung SDI', '삼성SDI'),
    '034020.KS': ('Doosan Enerbility', '두산에너빌리티'), '000810.KS': ('Samsung Fire', '삼성화재'),
    '047050.KS': ('Posco Int', '포스코인터내셔널'), '042700.KS': ('Hanmi Pharm', '한미약품'),
    '028670.KS': ('Pan Ocean', '팬오션'), '161390.KS': ('Hankook Tire', '한국타이어앤테크놀로지'),
    '002790.KS': ('Amore G', '아모레G'), '139480.KS': ('E-mart', '이마트'),
    '032640.KS': ('LG Uplus', 'LG유플러스'), '017670.KS': ('SK Telecom', 'SK텔레콤'),
    '030200.KS': ('KT', 'KT'), '014680.KS': ('Hansol', '한솔케미칼'),
    '251270.KS': ('Netmarble', '넷마블'), '001450.KS': ('Hyundai Marine', '현대해상'),
    '112040.KQ': ('Wemade', '위메이드'), '263750.KQ': ('Pearl Abyss', '펄어비스'),
    '066970.KQ': ('L&F', '엘앤에프'), '247540.KQ': ('Ecopro BM', '에코프로비엠'),
    '086520.KQ': ('Ecopro', '에코프로'), '028300.KQ': ('HLB', 'HLB'),
    '196170.KQ': ('Alteogen', '알테오젠'), '000120.KS': ('CJ Logistics', 'CJ대한통운'),
    '003490.KS': ('Korean Air', '대한항공'), '008770.KS': ('Hotel Shilla', '호텔신라'),
    '005300.KS': ('Lotte Chilsung', '롯데칠성'), '071050.KS': ('Korea Inv', '한국금융지주'),
    '039490.KS': ('Kiwoom', '키움증권'), '006800.KS': ('Mirae Asset', '미래에셋증권'),
    '001040.KS': ('CJ ENM', 'CJ ENM'), '036460.KS': ('KOGAS', '한국가스공사'),
    '000080.KS': ('HiteJinro', '하이트진로'), '042670.KS': ('HD Hyundai', 'HD현대'),
    '000100.KS': ('Yuhan', '유한양행'), '009830.KS': ('Hanwha Sol', '한화솔루션'),
    '112610.KS': ('CS Wind', 'CS윈드'), '282330.KS': ('BGF Retail', 'BGF리테일'),
    '020150.KS': ('Iljin', '일진머티리얼즈'), '011780.KS': ('Kumho Petro', '금호석유'),
    '001430.KS': ('SeAH Besteel', '세아베스틸지주')
}

us_etfs = {
    'SPY': ('SPDR S&P 500 ETF', 'S&P 500 ETF'), 'IVV': ('iShares Core S&P 500 ETF', 'S&P 500 ETF'),
    'VOO': ('Vanguard S&P 500 ETF', 'S&P 500 ETF'), 'QQQ': ('Invesco QQQ Trust', '나스닥 100 ETF'),
    'SCHD': ('Schwab US Dividend Equity ETF', 'SCHD 배당 ETF'), 'VTI': ('Vanguard Total Stock Market ETF', '미국 전체 주식 ETF'),
    'SOXX': ('iShares Semiconductor ETF', '반도체 ETF'), 'SMH': ('VanEck Semiconductor ETF', '반도체 ETF (SMH)'),
    'XLK': ('Technology Select Sector SPDR', '미국 기술주 ETF'), 'XLV': ('Health Care Select Sector', '미국 헬스케어 ETF'),
    'XLF': ('Financial Select Sector SPDR', '미국 금융주 ETF'), 'XLE': ('Energy Select Sector SPDR', '미국 에너지 ETF'),
    'ARKK': ('ARK Innovation ETF', 'ARK 혁신성장 ETF'), 'IWM': ('iShares Russell 2000 ETF', '러셀 2000 ETF'),
    'GLD': ('SPDR Gold Trust', '금 현물 ETF'), 'TLT': ('iShares 20+ Year Treasury Bond ETF', '미국 20년물 국채 ETF')
}

kr_etfs = {
    '381180.KS': ('TIGER US Phila Semi Nasdaq', 'TIGER 미국필라델피아반도체나스닥'),
    '446770.KS': ('ACE Global Semi TOP4 Plus', 'ACE 글로벌반도체TOP4 Plus'),
    '390390.KS': ('KODEX US Semiconductor', 'KODEX 미국반도체'),
    '497570.KS': ('TIGER US Phila AI Semi Nasdaq', 'TIGER 미국필라델피아AI반도체나스닥'),
    '487230.KS': ('KODEX US AI Power Infra', 'KODEX 미국AI전력핵심인프라'),
    '491010.KS': ('TIGER Global AI Power Infra', 'TIGER 글로벌AI전력인프라액티브'),
    '487320.KS': ('KODEX US AI Optical Network', 'KODEX 미국AI광통신네트워크'),
    '485530.KS': ('KODEX US Aerospace', 'KODEX 미국우주항공'),
    '481190.KS': ('SOL US Tech TOP10', 'SOL 미국테크TOP10'),
    '379800.KS': ('TIGER US Tech TOP10 INDXX', 'TIGER 미국테크TOP10 INDXX'),
    '465580.KS': ('ACE US Big Tech TOP7 Plus', 'ACE 미국빅테크TOP7 Plus'),
    '367380.KS': ('ACE US Nasdaq 100', 'ACE 미국나스닥100'),
    '360200.KS': ('ACE US S&P500', 'ACE 미국S&P500'),
    '446720.KS': ('SOL US Div Dow Jones', 'SOL 미국배당다우존스'),
    '402970.KS': ('ACE US Div Dow Jones', 'ACE 미국배당다우존스'),
    '148020.KS': ('RISE 200', 'RISE 200'),
    '161510.KS': ('PLUS High Dividend', 'PLUS 고배당주'),
    '466940.KS': ('TIGER Bank High Div Plus TOP10', 'TIGER 은행고배당플러스TOP10'),
    
    # 대표 K-ETF 추가
    '069500.KS': ('KODEX 200', 'KODEX 200'),
    '122630.KS': ('KODEX Leverage', 'KODEX 레버리지'),
    '114800.KS': ('KODEX Inverse', 'KODEX 인버스'),
    '305720.KS': ('KODEX 2nd Battery', 'KODEX 2차전지산업'),
    '364980.KS': ('TIGER KRX 2nd Battery K-New Deal', 'TIGER KRX2차전지K-뉴딜'),
    '133690.KS': ('TIGER US Nasdaq 100', 'TIGER 미국나스닥100'),
    '305540.KS': ('TIGER US S&P500', 'TIGER 미국S&P500'),
    '091160.KS': ('KODEX Semiconductor', 'KODEX 반도체'),
    '153130.KS': ('KODEX K-TOP 50', 'KODEX K-TOP 50')
}

us_str = "    'US': {\n" + ",\n".join([f"        '{k}': {{'en': '{v[0]}', 'ko': '{v[1]}'}}" for k, v in us_stocks.items()]) + "\n    },"
kr_str = "    'KR': {\n" + ",\n".join([f"        '{k}': {{'en': '{v[0]}', 'ko': '{v[1]}'}}" for k, v in kr_stocks.items()]) + "\n    },"
us_etf_str = "    'US_ETF': {\n" + ",\n".join([f"        '{k}': {{'en': '{v[0]}', 'ko': '{v[1]}'}}" for k, v in us_etfs.items()]) + "\n    },"
kr_etf_str = "    'KR_ETF': {\n" + ",\n".join([f"        '{k}': {{'en': '{v[0]}', 'ko': '{v[1]}'}}" for k, v in kr_etfs.items()]) + "\n    }"

stock_info_str = f"STOCK_INFO = {{\n{us_str}\n{kr_str}\n{us_etf_str}\n{kr_etf_str}\n}}"

with open('fetch_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace STOCK_INFO block
new_content = re.sub(r'STOCK_INFO = \{.*?\n\}\n', stock_info_str + '\n', content, flags=re.DOTALL)

with open('fetch_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated fetch_data.py successfully!")
