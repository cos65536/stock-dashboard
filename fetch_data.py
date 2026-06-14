import yfinance as yf
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import time

# 종목 리스트 및 도메인 설정 (Clearbit API 연동용)
STOCK_INFO = {
    'US': {
        'AAPL': {'en': 'Apple', 'ko': '애플'},
        'MSFT': {'en': 'Microsoft', 'ko': '마이크로소프트'},
        'GOOGL': {'en': 'Alphabet', 'ko': '구글'},
        'AMZN': {'en': 'Amazon', 'ko': '아마존'},
        'NVDA': {'en': 'NVIDIA', 'ko': '엔비디아'},
        'META': {'en': 'Meta', 'ko': '메타'},
        'TSLA': {'en': 'Tesla', 'ko': '테슬라'},
        'TSM': {'en': 'TSMC', 'ko': 'TSMC'},
        'AVGO': {'en': 'Broadcom', 'ko': '브로드컴'},
        'LLY': {'en': 'Eli Lilly', 'ko': '일라이 릴리'},
        'JPM': {'en': 'JPMorgan Chase', 'ko': 'JP모건'},
        'V': {'en': 'Visa', 'ko': '비자'},
        'WMT': {'en': 'Walmart', 'ko': '월마트'},
        'NFLX': {'en': 'Netflix', 'ko': '넷플릭스'},
        'AMD': {'en': 'AMD', 'ko': 'AMD'},
        'BRK-B': {'en': 'Berkshire Hathaway', 'ko': '버크셔 해서웨이'},
        'XOM': {'en': 'Exxon Mobil', 'ko': '엑슨 모빌'},
        'JNJ': {'en': 'Johnson & Johnson', 'ko': '존슨앤드존슨'},
        'PLTR': {'en': 'Palantir', 'ko': '팔란티어'},
        'QCOM': {'en': 'Qualcomm', 'ko': '퀄컴'},
        'COST': {'en': 'Costco', 'ko': '코스트코'},
        'DIS': {'en': 'Walt Disney', 'ko': '디즈니'},
        'CRM': {'en': 'Salesforce', 'ko': '세일즈포스'},
        'PG': {'en': 'Procter & Gamble', 'ko': 'P&G'},
        'MA': {'en': 'Mastercard', 'ko': '마스터카드'},
        'HD': {'en': 'Home Depot', 'ko': '홈디포'},
        'BAC': {'en': 'Bank of America', 'ko': '뱅크오브아메리카'},
        'ABBV': {'en': 'AbbVie', 'ko': '애브비'},
        'CVX': {'en': 'Chevron', 'ko': '쉐브론'},
        'KO': {'en': 'Coca-Cola', 'ko': '코카콜라'},
        'PEP': {'en': 'PepsiCo', 'ko': '펩시코'},
        'MRK': {'en': 'Merck', 'ko': '머크'},
        'TMO': {'en': 'Thermo Fisher', 'ko': '써모피셔'},
        'ADBE': {'en': 'Adobe', 'ko': '어도비'},
        'MCD': {'en': 'McDonalds', 'ko': '맥도날드'},
        'CSCO': {'en': 'Cisco', 'ko': '시스코'},
        'ACN': {'en': 'Accenture', 'ko': '액센츄어'},
        'ABT': {'en': 'Abbott Labs', 'ko': '애벗 연구소'},
        'LIN': {'en': 'Linde', 'ko': '린데'},
        'DHR': {'en': 'Danaher', 'ko': '다나허'},
        'TXN': {'en': 'Texas Instruments', 'ko': '텍사스 인스트루먼트'},
        'NEE': {'en': 'NextEra Energy', 'ko': '넥스테라 에너지'},
        'PFE': {'en': 'Pfizer', 'ko': '화이자'},
        'PM': {'en': 'Philip Morris', 'ko': '필립 모리스'},
        'WFC': {'en': 'Wells Fargo', 'ko': '웰스파고'},
        'COP': {'en': 'ConocoPhillips', 'ko': '코노코필립스'},
        'UNP': {'en': 'Union Pacific', 'ko': '유니온 퍼시픽'},
        'HON': {'en': 'Honeywell', 'ko': '허니웰'},
        'RTX': {'en': 'Raytheon', 'ko': '레이시온'},
        'INTC': {'en': 'Intel', 'ko': '인텔'},
        'BA': {'en': 'Boeing', 'ko': '보잉'},
        'IBM': {'en': 'IBM', 'ko': 'IBM'},
        'GE': {'en': 'General Electric', 'ko': 'GE'},
        'AMGN': {'en': 'Amgen', 'ko': '암젠'},
        'NOW': {'en': 'ServiceNow', 'ko': '서비스나우'},
        'SPGI': {'en': 'S&P Global', 'ko': 'S&P 글로벌'},
        'CAT': {'en': 'Caterpillar', 'ko': '캐터필라'},
        'C': {'en': 'Citigroup', 'ko': '씨티그룹'},
        'GS': {'en': 'Goldman Sachs', 'ko': '골드만삭스'},
        'INTU': {'en': 'Intuit', 'ko': '인튜이트'},
        'BKNG': {'en': 'Booking Holdings', 'ko': '부킹 홀딩스'},
        'UNH': {'en': 'UnitedHealth', 'ko': '유나이티드헬스'},
        'ISRG': {'en': 'Intuitive Surgical', 'ko': '인튜이티브 서지컬'},
        'SYK': {'en': 'Stryker', 'ko': '스트라이커'},
        'TJX': {'en': 'TJX Companies', 'ko': 'TJX'},
        'PGR': {'en': 'Progressive', 'ko': '프로그레시브'},
        'BSX': {'en': 'Boston Scientific', 'ko': '보스턴 사이언티픽'},
        'REGN': {'en': 'Regeneron', 'ko': '리제네론'},
        'CB': {'en': 'Chubb', 'ko': '처브'},
        'MDT': {'en': 'Medtronic', 'ko': '메드트로닉'},
        'MMC': {'en': 'Marsh & McLennan', 'ko': '마쉬앤맥레넌'},
        'MU': {'en': 'Micron Technology', 'ko': '마이크론'},
        'SO': {'en': 'Southern Co', 'ko': '서던 컴퍼니'},
        'ADP': {'en': 'Automatic Data', 'ko': 'ADP'},
        'FI': {'en': 'Fiserv', 'ko': '파이서브'},
        'BDX': {'en': 'Becton Dickinson', 'ko': '벡톤 디킨슨'},
        'ICE': {'en': 'Intercontinental Exchange', 'ko': 'ICE'},
        'CME': {'en': 'CME Group', 'ko': 'CME 그룹'},
        'WM': {'en': 'Waste Management', 'ko': '웨이스트 매니지먼트'},
        'AON': {'en': 'Aon', 'ko': '에이온'},
        'CL': {'en': 'Colgate-Palmolive', 'ko': '콜게이트'},
        'EOG': {'en': 'EOG Resources', 'ko': 'EOG 리소스'},
        'ITW': {'en': 'Illinois Tool', 'ko': '일리노이 툴'},
        'SLB': {'en': 'Schlumberger', 'ko': '슐럼버거'},
        'T': {'en': 'AT&T', 'ko': 'AT&T'},
        'VZ': {'en': 'Verizon', 'ko': '버라이즌'},
        'F': {'en': 'Ford', 'ko': '포드'},
        'GM': {'en': 'General Motors', 'ko': 'GM'},
        'KHC': {'en': 'Kraft Heinz', 'ko': '크래프트 하인즈'},
        'UBER': {'en': 'Uber', 'ko': '우버'},
        'ABNB': {'en': 'Airbnb', 'ko': '에어비앤비'},
        'SNOW': {'en': 'Snowflake', 'ko': '스노우플레이크'},
        'SHOP': {'en': 'Shopify', 'ko': '쇼피파이'},
        'SQ': {'en': 'Block', 'ko': '블록'},
        'PYPL': {'en': 'PayPal', 'ko': '페이팔'},
        'COIN': {'en': 'Coinbase', 'ko': '코인베이스'},
        'HOOD': {'en': 'Robinhood', 'ko': '로빈후드'},
        'ZM': {'en': 'Zoom', 'ko': '줌'},
        'RBLX': {'en': 'Roblox', 'ko': '로블록스'},
        'U': {'en': 'Unity', 'ko': '유니티'}
    },
    'KR': {
        '005930.KS': {'en': 'Samsung Electronics', 'ko': '삼성전자'},
        '000660.KS': {'en': 'SK Hynix', 'ko': 'SK하이닉스'},
        '373220.KS': {'en': 'LG Energy Solution', 'ko': 'LG에너지솔루션'},
        '207940.KS': {'en': 'Samsung Biologics', 'ko': '삼성바이오로직스'},
        '005380.KS': {'en': 'Hyundai Motor', 'ko': '현대차'},
        '000270.KS': {'en': 'Kia', 'ko': '기아'},
        '068270.KS': {'en': 'Celltrion', 'ko': '셀트리온'},
        '035420.KS': {'en': 'NAVER', 'ko': '네이버'},
        '035720.KS': {'en': 'Kakao', 'ko': '카카오'},
        '051910.KS': {'en': 'LG Chem', 'ko': 'LG화학'},
        '005490.KS': {'en': 'POSCO', 'ko': 'POSCO홀딩스'},
        '105560.KS': {'en': 'KB Financial', 'ko': 'KB금융'},
        '055550.KS': {'en': 'Shinhan Fin', 'ko': '신한지주'},
        '015760.KS': {'en': 'KEPCO', 'ko': '한국전력'},
        '012330.KS': {'en': 'Hyundai Mobis', 'ko': '현대모비스'},
        '066570.KS': {'en': 'LG Electronics', 'ko': 'LG전자'},
        '028260.KS': {'en': 'Samsung C&T', 'ko': '삼성물산'},
        '033780.KS': {'en': 'KT&G', 'ko': 'KT&G'},
        '051900.KS': {'en': 'LG H&H', 'ko': 'LG생활건강'},
        '034730.KS': {'en': 'SK', 'ko': 'SK'},
        '032830.KS': {'en': 'Samsung Life', 'ko': '삼성생명'},
        '011200.KS': {'en': 'HMM', 'ko': 'HMM'},
        '018260.KS': {'en': 'Samsung SDS', 'ko': '삼성SDS'},
        '096770.KS': {'en': 'SK Innovation', 'ko': 'SK이노베이션'},
        '010950.KS': {'en': 'S-Oil', 'ko': 'S-Oil'},
        '003550.KS': {'en': 'LG Corp', 'ko': 'LG'},
        '323410.KS': {'en': 'Kakao Bank', 'ko': '카카오뱅크'},
        '316140.KS': {'en': 'Woori Fin', 'ko': '우리금융지주'},
        '024110.KS': {'en': 'IBK', 'ko': '기업은행'},
        '377300.KS': {'en': 'Kakao Pay', 'ko': '카카오페이'},
        '259960.KS': {'en': 'Krafton', 'ko': '크래프톤'},
        '011170.KS': {'en': 'Lotte Chem', 'ko': '롯데케미칼'},
        '009150.KS': {'en': 'Samsung Electro-Mech', 'ko': '삼성전기'},
        '004020.KS': {'en': 'Hyundai Steel', 'ko': '현대제철'},
        '042660.KS': {'en': 'Hanwha Ocean', 'ko': '한화오션'},
        '010130.KS': {'en': 'Korea Zinc', 'ko': '고려아연'},
        '005830.KS': {'en': 'DB Insurance', 'ko': 'DB손해보험'},
        '011070.KS': {'en': 'LG Innotek', 'ko': 'LG이노텍'},
        '090430.KS': {'en': 'Amorepacific', 'ko': '아모레퍼시픽'},
        '036570.KS': {'en': 'NCSoft', 'ko': '엔씨소프트'},
        '021240.KS': {'en': 'Coway', 'ko': '코웨이'},
        '086280.KS': {'en': 'Hyundai Glovis', 'ko': '현대글로비스'},
        '078930.KS': {'en': 'Yuhan', 'ko': '유한양행'},
        '029780.KS': {'en': 'Samsung Card', 'ko': '삼성카드'},
        '271560.KS': {'en': 'Orion', 'ko': '오리온'},
        '010140.KS': {'en': 'Samsung Heavy', 'ko': '삼성중공업'},
        '028050.KS': {'en': 'Hanwha Aerospace', 'ko': '한화에어로스페이스'},
        '006400.KS': {'en': 'Samsung SDI', 'ko': '삼성SDI'},
        '034020.KS': {'en': 'Doosan Enerbility', 'ko': '두산에너빌리티'},
        '000810.KS': {'en': 'Samsung Fire', 'ko': '삼성화재'},
        '047050.KS': {'en': 'Posco Int', 'ko': '포스코인터내셔널'},
        '042700.KS': {'en': 'Hanmi Pharm', 'ko': '한미약품'},
        '028670.KS': {'en': 'Pan Ocean', 'ko': '팬오션'},
        '161390.KS': {'en': 'Hankook Tire', 'ko': '한국타이어앤테크놀로지'},
        '002790.KS': {'en': 'Amore G', 'ko': '아모레G'},
        '139480.KS': {'en': 'E-mart', 'ko': '이마트'},
        '032640.KS': {'en': 'LG Uplus', 'ko': 'LG유플러스'},
        '017670.KS': {'en': 'SK Telecom', 'ko': 'SK텔레콤'},
        '030200.KS': {'en': 'KT', 'ko': 'KT'},
        '014680.KS': {'en': 'Hansol', 'ko': '한솔케미칼'},
        '251270.KS': {'en': 'Netmarble', 'ko': '넷마블'},
        '001450.KS': {'en': 'Hyundai Marine', 'ko': '현대해상'},
        '112040.KQ': {'en': 'Wemade', 'ko': '위메이드'},
        '263750.KQ': {'en': 'Pearl Abyss', 'ko': '펄어비스'},
        '066970.KQ': {'en': 'L&F', 'ko': '엘앤에프'},
        '247540.KQ': {'en': 'Ecopro BM', 'ko': '에코프로비엠'},
        '086520.KQ': {'en': 'Ecopro', 'ko': '에코프로'},
        '028300.KQ': {'en': 'HLB', 'ko': 'HLB'},
        '196170.KQ': {'en': 'Alteogen', 'ko': '알테오젠'},
        '000120.KS': {'en': 'CJ Logistics', 'ko': 'CJ대한통운'},
        '003490.KS': {'en': 'Korean Air', 'ko': '대한항공'},
        '008770.KS': {'en': 'Hotel Shilla', 'ko': '호텔신라'},
        '005300.KS': {'en': 'Lotte Chilsung', 'ko': '롯데칠성'},
        '071050.KS': {'en': 'Korea Inv', 'ko': '한국금융지주'},
        '039490.KS': {'en': 'Kiwoom', 'ko': '키움증권'},
        '006800.KS': {'en': 'Mirae Asset', 'ko': '미래에셋증권'},
        '001040.KS': {'en': 'CJ ENM', 'ko': 'CJ ENM'},
        '036460.KS': {'en': 'KOGAS', 'ko': '한국가스공사'},
        '000080.KS': {'en': 'HiteJinro', 'ko': '하이트진로'},
        '042670.KS': {'en': 'HD Hyundai', 'ko': 'HD현대'},
        '000100.KS': {'en': 'Yuhan', 'ko': '유한양행'},
        '009830.KS': {'en': 'Hanwha Sol', 'ko': '한화솔루션'},
        '112610.KS': {'en': 'CS Wind', 'ko': 'CS윈드'},
        '282330.KS': {'en': 'BGF Retail', 'ko': 'BGF리테일'},
        '020150.KS': {'en': 'Iljin', 'ko': '일진머티리얼즈'},
        '011780.KS': {'en': 'Kumho Petro', 'ko': '금호석유'},
        '001430.KS': {'en': 'SeAH Besteel', 'ko': '세아베스틸지주'}
    },
    'US_ETF': {
        'SPY': {'en': 'SPDR S&P 500 ETF', 'ko': 'S&P 500 ETF'},
        'IVV': {'en': 'iShares Core S&P 500 ETF', 'ko': 'S&P 500 ETF'},
        'VOO': {'en': 'Vanguard S&P 500 ETF', 'ko': 'S&P 500 ETF'},
        'QQQ': {'en': 'Invesco QQQ Trust', 'ko': '나스닥 100 ETF'},
        'SCHD': {'en': 'Schwab US Dividend Equity ETF', 'ko': 'SCHD 배당 ETF'},
        'VTI': {'en': 'Vanguard Total Stock Market ETF', 'ko': '미국 전체 주식 ETF'},
        'SOXX': {'en': 'iShares Semiconductor ETF', 'ko': '반도체 ETF'},
        'SMH': {'en': 'VanEck Semiconductor ETF', 'ko': '반도체 ETF (SMH)'},
        'XLK': {'en': 'Technology Select Sector SPDR', 'ko': '미국 기술주 ETF'},
        'XLV': {'en': 'Health Care Select Sector', 'ko': '미국 헬스케어 ETF'},
        'XLF': {'en': 'Financial Select Sector SPDR', 'ko': '미국 금융주 ETF'},
        'XLE': {'en': 'Energy Select Sector SPDR', 'ko': '미국 에너지 ETF'},
        'ARKK': {'en': 'ARK Innovation ETF', 'ko': 'ARK 혁신성장 ETF'},
        'IWM': {'en': 'iShares Russell 2000 ETF', 'ko': '러셀 2000 ETF'},
        'GLD': {'en': 'SPDR Gold Trust', 'ko': '금 현물 ETF'},
        'TLT': {'en': 'iShares 20+ Year Treasury Bond ETF', 'ko': '미국 20년물 국채 ETF'}
    },
    'KR_ETF': {
        '381180.KS': {'en': 'TIGER US Phila Semi Nasdaq', 'ko': 'TIGER 미국필라델피아반도체나스닥'},
        '446770.KS': {'en': 'ACE Global Semi TOP4 Plus', 'ko': 'ACE 글로벌반도체TOP4 Plus'},
        '390390.KS': {'en': 'KODEX US Semiconductor', 'ko': 'KODEX 미국반도체'},
        '497570.KS': {'en': 'TIGER US Phila AI Semi Nasdaq', 'ko': 'TIGER 미국필라델피아AI반도체나스닥'},
        '487230.KS': {'en': 'KODEX US AI Power Infra', 'ko': 'KODEX 미국AI전력핵심인프라'},
        '491010.KS': {'en': 'TIGER Global AI Power Infra', 'ko': 'TIGER 글로벌AI전력인프라액티브'},
        '487320.KS': {'en': 'KODEX US AI Optical Network', 'ko': 'KODEX 미국AI광통신네트워크'},
        '485530.KS': {'en': 'KODEX US Aerospace', 'ko': 'KODEX 미국우주항공'},
        '481190.KS': {'en': 'SOL US Tech TOP10', 'ko': 'SOL 미국테크TOP10'},
        '379800.KS': {'en': 'TIGER US Tech TOP10 INDXX', 'ko': 'TIGER 미국테크TOP10 INDXX'},
        '465580.KS': {'en': 'ACE US Big Tech TOP7 Plus', 'ko': 'ACE 미국빅테크TOP7 Plus'},
        '367380.KS': {'en': 'ACE US Nasdaq 100', 'ko': 'ACE 미국나스닥100'},
        '360200.KS': {'en': 'ACE US S&P500', 'ko': 'ACE 미국S&P500'},
        '446720.KS': {'en': 'SOL US Div Dow Jones', 'ko': 'SOL 미국배당다우존스'},
        '402970.KS': {'en': 'ACE US Div Dow Jones', 'ko': 'ACE 미국배당다우존스'},
        '148020.KS': {'en': 'RISE 200', 'ko': 'RISE 200'},
        '161510.KS': {'en': 'PLUS High Dividend', 'ko': 'PLUS 고배당주'},
        '466940.KS': {'en': 'TIGER Bank High Div Plus TOP10', 'ko': 'TIGER 은행고배당플러스TOP10'},
        '069500.KS': {'en': 'KODEX 200', 'ko': 'KODEX 200'},
        '122630.KS': {'en': 'KODEX Leverage', 'ko': 'KODEX 레버리지'},
        '114800.KS': {'en': 'KODEX Inverse', 'ko': 'KODEX 인버스'},
        '305720.KS': {'en': 'KODEX 2nd Battery', 'ko': 'KODEX 2차전지산업'},
        '364980.KS': {'en': 'TIGER KRX 2nd Battery K-New Deal', 'ko': 'TIGER KRX2차전지K-뉴딜'},
        '133690.KS': {'en': 'TIGER US Nasdaq 100', 'ko': 'TIGER 미국나스닥100'},
        '305540.KS': {'en': 'TIGER US S&P500', 'ko': 'TIGER 미국S&P500'},
        '091160.KS': {'en': 'KODEX Semiconductor', 'ko': 'KODEX 반도체'},
        '153130.KS': {'en': 'KODEX K-TOP 50', 'ko': 'KODEX K-TOP 50'}
    }
}

def calculate_rsi(data, periods=14):
    close_delta = data['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 0

def get_naver_finance_info(code):
    # .KS, .KQ 제거하고 6자리 코드만 사용
    code = code.replace('.KS', '').replace('.KQ', '')
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    info = {}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        per_em = soup.select_one('#_per')
        pbr_em = soup.select_one('#_pbr')
        c_per_em = soup.select_one('#_cns_per')
        c_eps_em = soup.select_one('#_cns_eps')
        
        if per_em: info['per'] = float(per_em.text.replace(',', ''))
        if pbr_em: info['pbr'] = float(pbr_em.text.replace(',', ''))
        if c_per_em: info['forward_pe'] = float(c_per_em.text.replace(',', ''))
        if c_eps_em: info['forward_eps'] = float(c_eps_em.text.replace(',', ''))
    except Exception as e:
        print(f"  [Naver Finance Parsing Error] {code}: {e}")
        
    return info

def get_quarterly_financials(ticker_obj):
    try:
        inc = ticker_obj.quarterly_income_stmt
        if inc is None or inc.empty:
            return []
            
        financials = []
        dates = inc.columns
        for d in dates:
            try:
                rev = inc.loc['Total Revenue', d] if 'Total Revenue' in inc.index else 0
                op_inc = inc.loc['Operating Income', d] if 'Operating Income' in inc.index else 0
                if pd.isna(rev): rev = 0
                if pd.isna(op_inc): op_inc = 0
                
                financials.append({
                    'date': d.strftime('%Y-%m'),
                    'revenue': float(rev),
                    'operating_income': float(op_inc)
                })
            except Exception:
                pass
                
        financials.reverse()
        return financials
    except Exception as e:
        return []

def fetch_stock_data():
    results = []
    
    for country, stocks in STOCK_INFO.items():
        for ticker, data_dict in stocks.items():
            print(f"Fetching data for {ticker}...")
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                hist = stock.history(period="1y")
                if hist.empty:
                    print(f"  [Warning] No history found for {ticker}")
                    continue
                    
                current_price = hist['Close'].iloc[-1]
                high_52w = hist['High'].max()
                mdd = ((current_price - high_52w) / high_52w) * 100 if high_52w > 0 else 0
                
                weekly_closes = hist['Close'].resample('W').last().dropna().tolist()
                history_prices = [round(p, 2) for p in weekly_closes]
                
                rsi = calculate_rsi(hist)
                
                market_cap = info.get('marketCap', 0)
                currency = info.get('currency', 'USD')
                
                market_cap_usd = market_cap
                if currency == 'KRW':
                    market_cap_usd = market_cap / 1300
                
                # 기본적으로 yfinance에서 가져오기
                per = info.get('trailingPE', None)
                pbr = info.get('priceToBook', None)
                forward_eps = info.get('forwardEps', None)
                forward_pe = info.get('forwardPE', None)
                
                # 한국 주식일 경우, 네이버 금융 크롤링 결과로 보완 (데이터가 없을 때만)
                if country == 'KR':
                    naver_info = get_naver_finance_info(ticker)
                    if per is None: per = naver_info.get('per')
                    if pbr is None: pbr = naver_info.get('pbr')
                    if forward_eps is None: forward_eps = naver_info.get('forward_eps')
                    if forward_pe is None: forward_pe = naver_info.get('forward_pe')
                    
                financials = get_quarterly_financials(stock)
                
                results.append({
                    'ticker': ticker,
                    'name_en': data_dict['en'],
                    'name_ko': data_dict['ko'],
                    'market_cap': market_cap,
                    'market_cap_usd': market_cap_usd,
                    'currency': currency,
                    'current_price': round(current_price, 2),
                    'per': round(per, 2) if per is not None else None,
                    'pbr': round(pbr, 2) if pbr is not None else None,
                    'forward_eps': round(forward_eps, 2) if forward_eps is not None else None,
                    'forward_pe': round(forward_pe, 2) if forward_pe is not None else None,
                    'mdd': round(mdd, 2),
                    'rsi': round(rsi, 2),
                    'country': country,
                    'financials': financials,
                    'history_prices': history_prices
                })
                
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
                
            time.sleep(0.5) # API Rate Limit 방지용 딜레이

    results.sort(key=lambda x: x['market_cap_usd'], reverse=True)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("Data saved to data.json")

if __name__ == "__main__":
    fetch_stock_data()
