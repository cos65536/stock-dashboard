document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    // DOM
    const loader = document.getElementById('loader');
    const content = document.getElementById('content');
    const stockGrid = document.getElementById('stock-grid');
    const noResults = document.getElementById('no-results');
    
    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    // Sliders & Search & Sort
    const sliderPer = document.getElementById('slider-per');
    const sliderPbr = document.getElementById('slider-pbr');
    const sliderMdd = document.getElementById('slider-mdd');
    const valPer = document.getElementById('val-per');
    const valPbr = document.getElementById('val-pbr');
    const valMdd = document.getElementById('val-mdd');
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const resultCount = document.getElementById('result-count');

    // Controls
    const langToggleBtn = document.getElementById('lang-toggle');
    const langText = document.getElementById('lang-text');
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    let allData = [];
    let currentLang = 'KO';
    let currentTab = 'US';

    const t = {
        'KO': {
            subtitle: '글로벌 주식 가치 평가 및 주요 지표 대시보드',
            loading: '데이터 불러오는 중...',
            fetching: '최신 시장 데이터를 가져오는 중입니다...',
            loaded: '최신 데이터 업데이트 완료',
            failed: '데이터 로드 실패. fetch_data.py를 먼저 실행해주세요.',
            advFilters: '상세 필터 조건',
            found: '종목 검색됨',
            usMarket: '미국 주식 시장',
            krMarket: '한국 주식 시장',
            noMatch: '조건에 맞는 주식이 없습니다.',
            cap: '시총',
            metricPer: 'PER (TTM)',
            metricPbr: 'PBR',
            metricMdd: 'MDD (고점대비)',
            metricRsi: 'RSI (14일)',
            metricFwdPe: 'FWD PER (12M)',
            metricFwdEps: 'FWD EPS (12M)',
            chartTitle: '최근 분기 실적 추이',
            rev: '매출',
            op: '영업이익',
            searchPlaceholder: '종목명 또는 티커 검색...',
            sortCap: '시가총액 순',
            sortPer: 'PER 낮은 순',
            sortPbr: 'PBR 낮은 순',
            sortMdd: 'MDD 큰 순 (고점대비 하락률)',
            usEtfMarket: '미국 ETF',
            krEtfMarket: '한국 ETF'
        },
        'EN': {
            subtitle: 'Global Stock Valuation & Metrics',
            loading: 'Data loading...',
            fetching: 'Fetching latest market data...',
            loaded: 'Live Data Loaded',
            failed: 'Failed to load data.',
            advFilters: 'Advanced Filters',
            found: 'stocks found',
            usMarket: 'US Market',
            krMarket: 'KR Market',
            noMatch: 'No stocks match the selected filters.',
            cap: 'Cap',
            metricPer: 'PER (TTM)',
            metricPbr: 'PBR',
            metricMdd: 'MDD (from ATH)',
            metricRsi: 'RSI (14)',
            metricFwdPe: 'FWD PER (12M)',
            metricFwdEps: 'FWD EPS (12M)',
            chartTitle: 'Recent Quarterly Financials',
            rev: 'Revenue',
            op: 'Operating Inc.',
            searchPlaceholder: 'Search ticker or company name...',
            sortCap: 'Market Cap (High to Low)',
            sortPer: 'PER (Low to High)',
            sortPbr: 'PBR (Low to High)',
            sortMdd: 'MDD (Largest Drop)',
            usEtfMarket: 'US ETF',
            krEtfMarket: 'KR ETF'
        }
    };

    const updateUIText = () => {
        const dict = t[currentLang];
        document.getElementById('t-subtitle').textContent = dict.subtitle;
        document.getElementById('t-advanced-filters').textContent = dict.advFilters;
        
        const elUs = document.getElementById('t-tab-us');
        if (elUs) elUs.textContent = dict.usMarket;
        
        const elKr = document.getElementById('t-tab-kr');
        if (elKr) elKr.textContent = dict.krMarket;
        
        const elUsEtf = document.getElementById('t-tab-us-etf');
        if (elUsEtf) elUsEtf.textContent = dict.usEtfMarket;
        
        const elKrEtf = document.getElementById('t-tab-kr-etf');
        if (elKrEtf) elKrEtf.textContent = dict.krEtfMarket;
        
        document.getElementById('search-input').placeholder = dict.searchPlaceholder;
        document.getElementById('t-sort-cap').textContent = dict.sortCap;
        document.getElementById('t-sort-per').textContent = dict.sortPer;
        document.getElementById('t-sort-pbr').textContent = dict.sortPbr;
        document.getElementById('t-sort-mdd').textContent = dict.sortMdd;
        
        document.getElementById('t-no-results').textContent = dict.noMatch;
        
        if(loader.style.display !== 'none') {
            document.getElementById('t-fetching').textContent = dict.fetching;
        }
        langText.textContent = currentLang;
    };

    const formatNumber = (num, lang = currentLang) => {
        if (num === null || num === undefined) return 'N/A';
        if (lang === 'KO') {
            if (num >= 1e12) return (num / 1e12).toFixed(2) + '조';
            if (num >= 1e8) return (num / 1e8).toFixed(2) + '억';
            return num.toLocaleString(undefined, { maximumFractionDigits: 0 });
        } else {
            if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
            if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
            if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
            return num.toLocaleString(undefined, { maximumFractionDigits: 0 });
        }
    };
    
    const formatShortNum = (num) => {
        if (num >= 1e12) return (num / 1e12).toFixed(1) + 'T';
        if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B';
        if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M';
        return num.toLocaleString();
    };

    const getColors = {
        per: (v) => !v ? 'val-neutral' : v < 15 ? 'val-excellent' : v <= 25 ? 'val-good' : v <= 35 ? 'val-neutral' : 'val-bad',
        pbr: (v) => !v ? 'val-neutral' : v < 1.0 ? 'val-excellent' : v <= 2 ? 'val-good' : v <= 4 ? 'val-neutral' : 'val-bad',
        mdd: (v) => v === null ? 'val-neutral' : v > -5 ? 'val-worst' : v > -15 ? 'val-neutral' : v > -30 ? 'val-good' : 'val-excellent',
        rsi: (v) => !v ? 'val-neutral' : v < 30 ? 'val-excellent' : v <= 40 ? 'val-good' : v <= 70 ? 'val-neutral' : v > 80 ? 'val-worst' : 'val-bad'
    };

    const generateSparklineHTML = (prices) => {
        if (!prices || prices.length < 2) return '';
        const width = 110; const height = 25;
        const maxPrice = Math.max(...prices);
        const minPrice = Math.min(...prices);
        const range = maxPrice - minPrice || 1;
        
        const points = prices.map((price, i) => {
            const x = (i / (prices.length - 1)) * width;
            const y = height - ((price - minPrice) / range) * height;
            return `${x},${y}`;
        }).join(' ');

        const isUp = prices[prices.length - 1] >= prices[0];
        const color = isUp ? 'var(--val-good)' : 'var(--val-bad)';

        return `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" style="margin-top: 0.5rem; overflow: visible;">
            <polyline points="${points}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    };

    const generateChartHTML = (financials, dict) => {
        if (!financials || financials.length === 0) return '';
        
        let maxVal = 0;
        financials.forEach(f => {
            if (f.revenue > maxVal) maxVal = f.revenue;
            if (f.operating_income > maxVal) maxVal = f.operating_income;
        });
        if (maxVal === 0) maxVal = 1;

        let barsHTML = '';
        financials.forEach(f => {
            let revRatio = f.revenue / maxVal;
            let opRatio = f.operating_income / maxVal;
            if (revRatio < 0) revRatio = 0.02;
            if (opRatio < 0) opRatio = 0.02;
            
            const revHeightPx = Math.max(revRatio * 100, 2); 
            const opHeightPx = Math.max(opRatio * 100, 2);
            const d = new Date(f.date + '-01');
            const qStr = d.getFullYear().toString().slice(2) + 'Q' + Math.ceil((d.getMonth()+1)/3);

            barsHTML += `
                <div class="bar-wrapper" style="display: flex; flex-direction: column; flex: 1;">
                    <div class="bar-group" style="display: flex; gap: 4px; align-items: flex-end; height: 100px; position: relative; justify-content: center;">
                        <div class="bar-tooltip">
                            ${f.date}<br>${dict.rev}: ${formatShortNum(f.revenue)}<br>${dict.op}: ${formatShortNum(f.operating_income)}
                        </div>
                        <div style="width: 14px; background-color: var(--accent-blue); opacity: 0.8; height: ${revHeightPx}px; border-radius: 3px 3px 0 0; transition: height 0.3s ease;"></div>
                        <div style="width: 14px; background-color: var(--accent-cyan); height: ${opHeightPx}px; border-radius: 3px 3px 0 0; transition: height 0.3s ease;"></div>
                    </div>
                    <div class="q-label" style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 0.5rem; font-weight: 600;">${qStr}</div>
                </div>
            `;
        });

        return `
            <div class="financials-chart" style="display: flex; flex-direction: column; gap: 1rem; padding-top: 1rem; border-top: 1px solid var(--card-border); margin-top: 0.5rem;">
                <div class="chart-header" style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.5rem; font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">
                    <span style="white-space: nowrap;">${dict.chartTitle}</span>
                    <div class="chart-legend" style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        <div class="legend-item" style="display: flex; align-items: center; gap: 0.25rem; white-space: nowrap;"><div style="width: 8px; height: 8px; border-radius: 50%; background: var(--accent-blue);"></div>${dict.rev}</div>
                        <div class="legend-item" style="display: flex; align-items: center; gap: 0.25rem; white-space: nowrap;"><div style="width: 8px; height: 8px; border-radius: 50%; background: var(--accent-cyan);"></div>${dict.op}</div>
                    </div>
                </div>
                <div class="bars-container" style="display: flex; gap: 0.5rem; height: 100px; align-items: flex-end; justify-content: space-between; margin-top: 0.5rem;">
                    ${barsHTML}
                </div>
            </div>
        `;
    };

    const createStockCard = (stock, dict) => {
        const card = document.createElement('div');
        card.className = 'stock-card';
        const stockName = currentLang === 'KO' ? stock.name_ko : stock.name_en;
        
        // Remove decimals from KRW
        const priceStr = stock.current_price.toLocaleString(undefined, { 
            minimumFractionDigits: stock.currency === 'KRW' ? 0 : 2, 
            maximumFractionDigits: stock.currency === 'KRW' ? 0 : 2 
        });

        card.innerHTML = `
            <div class="card-header">
                <div class="stock-info">
                    <span class="name" title="${stockName}">${stockName}</span>
                    <div class="ticker-wrap">
                        <span class="ticker">${stock.ticker.replace('.KS', '')}</span>
                        <span class="country-badge" style="color: ${stock.country === 'US' ? 'var(--accent-blue)' : 'var(--val-good)'}">${stock.country}</span>
                    </div>
                </div>
                <div class="price-info">
                    <div>
                        <span class="price">${priceStr}</span>
                        <span class="currency">${stock.currency}</span>
                    </div>
                    <div class="market-cap">${dict.cap}: ${formatNumber(stock.market_cap, currentLang)}</div>
                    ${generateSparklineHTML(stock.history_prices)}
                </div>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <span class="metric-label">${dict.metricPer}</span>
                    <span class="metric-value ${getColors.per(stock.per)}">${stock.per !== null ? stock.per : 'N/A'}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">${dict.metricFwdPe}</span>
                    <span class="metric-value ${getColors.per(stock.forward_pe)}">${stock.forward_pe !== null ? stock.forward_pe : 'N/A'}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">${dict.metricFwdEps}</span>
                    <span class="metric-value ${stock.forward_eps > 0 ? 'val-good' : 'val-neutral'}">${stock.forward_eps !== null ? stock.forward_eps.toLocaleString() : 'N/A'}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">${dict.metricPbr}</span>
                    <span class="metric-value ${getColors.pbr(stock.pbr)}">${stock.pbr !== null ? stock.pbr : 'N/A'}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">${dict.metricMdd}</span>
                    <span class="metric-value ${getColors.mdd(stock.mdd)}">${stock.mdd !== null ? stock.mdd + '%' : 'N/A'}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">${dict.metricRsi}</span>
                    <span class="metric-value ${getColors.rsi(stock.rsi)}">${stock.rsi !== null ? stock.rsi : 'N/A'}</span>
                </div>
            </div>
            ${generateChartHTML(stock.financials, dict)}
        `;
        return card;
    };

    const renderStocks = (data) => {
        stockGrid.innerHTML = '';
        const dict = t[currentLang];
        
        // Filter by Tab (US or KR)
        const tabData = data.filter(s => s.country === currentTab);
        
        if (tabData.length === 0) {
            noResults.style.display = 'flex';
        } else {
            noResults.style.display = 'none';
            tabData.forEach(s => stockGrid.appendChild(createStockCard(s, dict)));
        }
        
        resultCount.textContent = `${tabData.length} ${dict.found}`;
    };

    // Filter Logic
    const applyFilters = () => {
        const maxPer = parseInt(sliderPer.value);
        const maxPbr = parseFloat(sliderPbr.value);
        const maxMdd = parseInt(sliderMdd.value);
        const searchTerm = searchInput.value.toLowerCase().trim();

        let filtered = allData.filter(s => {
            const passPer = (maxPer === 100) || (s.per !== null && s.per <= maxPer);
            const passPbr = (maxPbr === 15) || (s.pbr !== null && s.pbr <= maxPbr);
            const passMdd = (maxMdd === 0) || (s.mdd !== null && s.mdd <= maxMdd);
            
            let passSearch = true;
            if (searchTerm) {
                const nameEn = (s.name_en || '').toLowerCase();
                const nameKo = (s.name_ko || '').toLowerCase();
                const ticker = (s.ticker || '').toLowerCase();
                passSearch = nameEn.includes(searchTerm) || nameKo.includes(searchTerm) || ticker.includes(searchTerm);
            }
            
            return passPer && passPbr && passMdd && passSearch;
        });
        
        const sortVal = sortSelect.value;
        filtered.sort((a, b) => {
            if (sortVal === 'cap_desc') return b.market_cap_usd - a.market_cap_usd;
            if (sortVal === 'per_asc') {
                const valA = a.per !== null ? a.per : 9999;
                const valB = b.per !== null ? b.per : 9999;
                return valA - valB;
            }
            if (sortVal === 'pbr_asc') {
                const valA = a.pbr !== null ? a.pbr : 9999;
                const valB = b.pbr !== null ? b.pbr : 9999;
                return valA - valB;
            }
            if (sortVal === 'mdd_asc') {
                const valA = a.mdd !== null ? a.mdd : 0;
                const valB = b.mdd !== null ? b.mdd : 0;
                return valA - valB; // Negative values, so smaller number means larger drop
            }
            return 0;
        });

        renderStocks(filtered);
    };

    // Tab Events
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            tabBtns.forEach(b => b.classList.remove('active'));
            // handle span click inside button
            const targetBtn = e.target.closest('.tab-btn');
            targetBtn.classList.add('active');
            currentTab = targetBtn.getAttribute('data-tab');
            applyFilters();
        });
    });

    // Events for Sliders & Inputs
    [sliderPer, sliderPbr, sliderMdd].forEach(slider => {
        slider.addEventListener('input', (e) => {
            const val = e.target.value;
            if(e.target.id === 'slider-per') valPer.textContent = val == 100 ? 'Any' : `≤ ${val}`;
            if(e.target.id === 'slider-pbr') valPbr.textContent = val == 15 ? 'Any' : `≤ ${val}`;
            if(e.target.id === 'slider-mdd') valMdd.textContent = val == 0 ? 'Any' : `≤ ${val}%`;
            applyFilters();
        });
    });
    
    searchInput.addEventListener('input', applyFilters);
    sortSelect.addEventListener('change', applyFilters);

    langToggleBtn.addEventListener('click', () => {
        currentLang = currentLang === 'KO' ? 'EN' : 'KO';
        updateUIText();
        applyFilters(); 
    });

    const setTheme = (theme) => {
        htmlElement.setAttribute('data-theme', theme);
        themeToggleBtn.innerHTML = `<i data-lucide="${theme === 'dark' ? 'sun' : 'moon'}"></i>`;
        lucide.createIcons();
    };

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        setTheme('light');
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        setTheme(event.matches ? "dark" : "light");
    });

    const loadData = async () => {
        try {
            updateUIText();
            const response = await fetch('data.json?t=' + new Date().getTime());
            if (!response.ok) throw new Error('Network response was not ok');
            
            allData = await response.json();
            
            applyFilters();
            
            loader.style.display = 'none';
            content.style.display = 'block'; // Show sections
            
            const dict = t[currentLang];
            document.getElementById('last-updated').innerHTML = `<i data-lucide="check-circle" style="color: var(--val-good)"></i> <span>${dict.loaded}</span>`;
            lucide.createIcons();
            
        } catch (error) {
            console.error('Error fetching data:', error);
            const dict = t[currentLang];
            loader.innerHTML = `
                <i data-lucide="alert-triangle" style="width: 40px; height: 40px; color: var(--val-bad);"></i>
                <p style="color: var(--val-bad)">${dict.failed}</p>
            `;
            lucide.createIcons();
        }
    };

    updateUIText();
    loadData();
});
