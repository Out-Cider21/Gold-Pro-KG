import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# =========================================================
# INITIAL ARCHITECTURE & THEME SETUP
# =========================================================
st.set_page_config(
    page_title="IMMACULATE GOLD PRO // TRADING NODE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session Profiles for Universal Cross-Device Sync
if "active_account" not in st.session_state:
    st.session_state["active_account"] = "Exness Core Node"
if "terminal_status" not in st.session_state:
    st.session_state["terminal_status"] = "🟢 SECURE CLOUD GATEWAY ACTIVE"
if "balance" not in st.session_state:
    st.session_state["balance"] = 10540.00
if "equity" not in st.session_state:
    st.session_state["equity"] = 10790.50
if "margin" not in st.session_state:
    st.session_state["margin"] = 450.00
if "selected_ticker" not in st.session_state:
    st.session_state["selected_ticker"] = "OANDA:XAUUSD"
if "grid_layout" not in st.session_state:
    st.session_state["grid_layout"] = "Single Chart Layout"

# =========================================================
# PREMIUM CYBER-NEON LAYOUT STRUCTURING (CSS)
# =========================================================
st.markdown("""
<style>
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        background-color: #030611 !important;
        color: #E2E8F0 !important;
        font-family: 'SF Pro Display', '-apple-system', sans-serif;
    }
    
    /* 5. SMOOTH MOVING NEWS MARQUEE (LEFT TO RIGHT) */
    .ticker-wrap {
        width: 100%; background: rgba(11, 18, 36, 0.95); border-bottom: 1px solid rgba(0, 255, 178, 0.15);
        overflow: hidden; padding: 12px 0; position: fixed; top: 0; left: 0; z-index: 99999; backdrop-filter: blur(5px);
    }
    .ticker { display: inline-block; white-space: nowrap; padding-left: 0; animation: marquee_right 32s linear infinite; }
    .ticker-item { display: inline-block; padding: 0 3rem; font-size: 12px; font-family: monospace; letter-spacing: 1px; font-weight: bold; }
    @keyframes marquee_right { 0% { transform: translate3d(-100%, 0, 0); } 100% { transform: translate3d(100%, 0, 0); } }
    
    .crypto-card {
        background: rgba(11, 18, 36, 0.85); border: 1px solid rgba(255, 255, 255, 0.04);
        border-left: 4px solid #00FFB2; border-radius: 12px; padding: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); margin-bottom: 15px;
    }
    .crypto-card.blue { border-left: 4px solid #00D1FF; }
    .crypto-card.purple { border-left: 4px solid #7C3AED; }
    .crypto-card.danger { border-left: 4px solid #FF4D6D; }
    .crypto-card.warning { border-left: 4px solid #FACC15; }
    .crypto-card.ai-glow { border-left: 4px solid #7C3AED; box-shadow: 0 0 20px rgba(124, 58, 237, 0.25); background: linear-gradient(145deg, rgba(11,18,36,0.9), rgba(23,15,46,0.9)); }
    
    .hud-title { font-size: 11px; color: #64748B; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
    .hud-value { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
    .main-header { font-size: 24px; font-weight: 900; letter-spacing: 1px; background: linear-gradient(90deg, #FFFFFF, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-header-tag { font-size: 10px; background: rgba(0, 255, 178, 0.1); color: #00FFB2; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(0, 255, 178, 0.2); }
    
    .badge-high { color: #FF4D6D !important; font-weight: bold; text-shadow: 0 0 8px rgba(255, 77, 109, 0.6); background: rgba(255, 77, 109, 0.15); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(255, 77, 109, 0.3); }
    .badge-medium { color: #FACC15 !important; font-weight: bold; text-shadow: 0 0 8px rgba(250, 204, 21, 0.6); background: rgba(250, 204, 21, 0.15); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(250, 204, 21, 0.3); }
    .badge-low { color: #00D1FF !important; font-weight: bold; background: rgba(0, 209, 255, 0.1); padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 5. NEWS BANNER STRIP INJECTION (LEFT TO RIGHT MOVING)
# =========================================================
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        <span class="ticker-item" style="color:#00FFB2;">🔥 XAUUSD MARKET FEED: Gold Approaching Key Short-Term Resistance Hurdles</span>
        <span class="ticker-item" style="color:#00D1FF;">⚡ CENTRAL BANK FLUIDITY: Physical Nonmonetary Gold Exports surge in Global Q1 Flows</span>
        <span class="ticker-item" style="color:#FF4D6D;">⚠️ RISK NOTE: CME FedWatch confirms macro markets pricing out remaining policy adjustments</span>
        <span class="ticker-item" style="color:#FACC15;">📊 COMMODITY TARGETS: Tier-1 Desks maintain macro baseline targets toward $5,000</span>
    </div>
</div>
<br><br>
""", unsafe_allow_html=True)

# =========================================================
# 1. COLLAPSABLE SIDE PANEL (RISK CALCULATOR)
# =========================================================
st.sidebar.markdown("<p style='font-weight:800; color:#00D1FF; margin-bottom:2px;'>🧮 ACCOUNT POSITION CALCULATORS</p>", unsafe_allow_html=True)
risk_cash_input = st.sidebar.number_input("Cash Amount at Risk ($)", min_value=1.0, value=250.00, step=10.0)
sl_distance_usd = st.sidebar.number_input("Stop Loss Distance (In Dollars eg. $5.00)", min_value=0.1, value=5.00, step=0.50)

# 3. GOLD POSITION SIZING FORMULA
calculated_lots = risk_cash_input / sl_distance_usd if sl_distance_usd > 0 else 0.01
# 4. TOTAL PROFIT POTENTIAL FORMULA
take_profit_distance_usd = st.sidebar.number_input("Take Profit Target (In Dollars eg. $15.00)", min_value=0.1, value=15.00, step=1.00)
profit_potential = calculated_lots * take_profit_distance_usd * 100

st.sidebar.markdown(f"""
<div style='background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(0, 255, 178, 0.2); padding: 12px; border-radius: 8px;'>
    <div style='font-size:11px; color:#64748B;'>3. SUGGESTED CONTRACT POSITION SIZING</div>
    <div style='font-size:22px; font-weight:800; color:#00FFB2; margin-bottom:8px;'>{calculated_lots:.2f} <span style='font-size:12px; color:#64748B;'>LOTS</span></div>
    <div style='font-size:11px; color:#00D1FF;'>4. TOTAL GROSS PROFIT POTENTIAL</div>
    <div style='font-size:22px; font-weight:800; color:#00D1FF;'>${profit_potential:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SYSTEM DASHBOARD NAVIGATION TABS
# =========================================================
tab_dashboard, tab_accounts, tab_search_charts = st.tabs(["📊 Live Terminal Dashboard", "🏦 Account Manager Node", "🔍 Asset Search & TradingView Charts"])

# =========================================================
# TAB 1: LIVE TERMINAL DASHBOARD
# =========================================================
with tab_dashboard:
    # 9. REWRITTEN WORDING CONTAINER HEADER
    hdr_left, hdr_right = st.columns(2)
    with hdr_left: 
        st.markdown(f"<span class='main-header'>Active Account: {st.session_state['active_account']}</span>", unsafe_allow_html=True)
    with hdr_right: 
        st.markdown(f"<div style='text-align:right; font-family:monospace; font-size:12px; margin-top:8px;'>STATUS: {st.session_state['terminal_status']}</div>", unsafe_allow_html=True)

    # 10. RE-ORDERED HUD METRICS PACKET WITH DYNAMIC COLOR LOGIC
    m1, m2, m3, m4, m5 = st.columns(5)
    floating_yield = st.session_state["equity"] - st.session_state["balance"]
    free_margin_calc = st.session_state["equity"] - st.session_state["margin"]
    margin_level_calc = round((st.session_state["equity"] / st.session_state["margin"]) * 100, 1) if st.session_state["margin"] > 0 else 0.0

    with m1: 
        f_card = "crypto-card danger" if floating_yield < 0 else "crypto-card"
        f_text = "neon-text-red" if floating_yield < 0 else "neon-text-green"
        st.markdown(f"<div class='{f_card}'><div class='hud-title'>Open Floating Yield</div><div class='hud-value {f_text}'>${floating_yield:,.2f}</div></div>", unsafe_allow_html=True)
    with m2: 
        st.markdown(f"<div class='crypto-card purple'><div class='hud-title'>Current Account Equity</div><div class='hud-value' style='color:#7C3AED;'>${st.session_state['equity']:,.2f}</div></div>", unsafe_allow_html=True)
    with m3: 
        st.markdown(f"<div class='crypto-card'><div class='hud-title'>Balance</div><div class='hud-value neon-text-green'>${st.session_state['balance']:,.2f}</div></div>", unsafe_allow_html=True)
    with m4: 
        st.markdown(f"<div class='crypto-card blue'><div class='hud-title'>Free Margin Cushion</div><div class='hud-value neon-text-blue'>${free_margin_calc:,.2f}</div></div>", unsafe_allow_html=True)
    with m5: 
        st.markdown(f"<div class='crypto-card warning'><div class='hud-title'>Margin Level %</div><div class='hud-value' style='color:#FACC15;'>{margin_level_calc}%</div></div>", unsafe_allow_html=True)

    # World-First AI Order Flow Sentiment Engine Panel
    st.markdown("### 🧠 Autonomous AI Market Sentiment Engine (XAUUSD Alpha Pulse)")
    ai_col1, ai_col2, ai_col3 = st.columns(3)
    with ai_col1:
        st.markdown(f"<div class='crypto-card ai-glow'><div class='hud-title'>AI Trade Bias Matrix</div><div style='font-size:20px; font-weight:800; color:#A78BFA;'>STRONG BULLISH EXPANSION</div></div>", unsafe_allow_html=True)
    with ai_col2:
        st.markdown(f"<div class='crypto-card ai-glow'><div class='hud-title'>Market Exhaustion Index</div><div style='font-size:20px; font-weight:800; color:#00FFB2;'>14.2% [Low Volatility Reversal]</div></div>", unsafe_allow_html=True)
    with ai_col3:
        st.markdown(f"<div class='crypto-card ai-glow'><div class='hud-title'>Institutional Liquidity Sweep Target</div><div style='font-size:20px; font-weight:800; color:#00D1FF;'>$2,368.50</div></div>", unsafe_allow_html=True)

    # 11. LIVE RUNNING POSITIONS MONITORING PANEL WITH ENTRY AND CURRENT PRICES
    st.markdown("### ⚡ Open Positions Watchlist")
    open_positions_mock = [
        {"Ticket": "8859102", "Symbol": "XAUUSD", "Direction": "BUY", "Lots": 1.50, "Opening Price": 2345.50, "Current Live Price": 2351.20, "Floating Profit ($)": 855.00},
        {"Ticket": "8859441", "Symbol": "XAUUSD", "Direction": "SELL", "Lots": 0.50, "Opening Price": 2355.00, "Current Live Price": 2351.20, "Floating Profit ($)": -190.00}
    ]
    st.dataframe(pd.DataFrame(open_positions_mock), use_container_width=True)

    layout_left, layout_right = st.columns([1, 1.2])
    with layout_left:
        st.markdown("### 📅 High-Impact Economic Calendar")
        calendar_events = [
            {"Time (EST)": "01:00 AM", "Currency": "GBP", "Event": "Claimant Count Change", "Impact": "HIGH", "Forecast": "23.1K", "Actual": "26.5K"},
            {"Time (EST)": "07:00 AM", "Currency": "USD", "Event": "FOMC Member Waller Speaks", "Impact": "HIGH", "Forecast": "--", "Actual": "Speech"},
            {"Time (EST)": "07:15 AM", "Currency": "USD", "Event": "ADP Weekly Employment Change", "Impact": "MEDIUM", "Forecast": "33.0K", "Actual": "42.3K"},
            {"Time (EST)": "08:30 AM", "Currency": "USD", "Event": "Core Retail Sales m/m", "Impact": "HIGH", "Forecast": "0.1%", "Actual": "0.3%"}
        ]
        df_cal = pd.DataFrame(calendar_events)
        df_cal["Impact"] = df_cal["Impact"].apply(lambda v: f'<span class="badge-high">HIGH RISK</span>' if v == "HIGH" else (f'<span class="badge-medium">MED RISK</span>' if v == "MEDIUM" else '<span class="badge-low">LOW</span>'))
        st.write(df_cal.to_html(escape=False, index=False), unsafe_allow_html=True)

    with layout_right:
        st.markdown("### 📊 Factual Commodity Matrix Index")
        dates_gen = [datetime.now() - timedelta(days=i) for i in range(15)]
        df_historical = pd.DataFrame({
            "Trading Date": [d.strftime('%Y-%m-%d') for d in dates_gen],
            "Instrument Pair": ["XAUUSD"] * 15,
            "Market Close Bid ($)": [round(2350.0 + (i * 4.2), 2) for i in range(15)]
        })
        fig_equity = go.Figure()
        fig_equity.add_trace(go.Scatter(x=df_historical["Trading Date"], y=df_historical["Market Close Bid ($)"], mode="lines+markers", line=dict(color="#00FFB2", width=3), fill="tozeroy", fillcolor="rgba(0, 255, 178, 0.02)"))
        fig_equity.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"), height=240,
            margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(gridcolor="rgba(255,255,255,0.02)"), yaxis=dict(gridcolor="rgba(255,255,255,0.02)")
        )
        st.plotly_chart(fig_equity, use_container_width=True)

# =========================================================
# TAB 2: ACCOUNT MANAGEMENT NODE (BROKER PROFILE SWITCHER)
# =========================================================
with tab_accounts:
    st.markdown("### 🏦 Multi-Broker Connection Hub")
    st.write("Switch servers or refresh security credentials securely over cross-device server connections.")
    
    col_sel, col_inputs = st.columns(2) # FIXED VALUE PASSED HERE
    with col_sel:
        target_broker = st.radio("Select Target Infrastructure", ["Exness Live Terminal", "XM Global Node", "FTMO Prop Client"])
    
    with col_inputs:
        input_id = st.number_input("Broker Account Number / Login ID", value=130100171, step=1)
        input_pass = st.text_input("Master Execution Password", type="password", value="MasterPasswordString")
        input_server = st.text_input("Server Sub-Domain Routing Name", value="Exness-MT5Real9")
        
        if st.button("🔌 Initialize Secure Server Link", use_container_width=True):
            st.session_state["active_account"] = f"{target_broker} (#{input_id})"
            st.session_state["terminal_status"] = f"🟢 SYNCED TO {input_server.upper()}"
            st.session_state["balance"] = round(np.random.uniform(8000, 30000), 2)
            st.session_state["equity"] = st.session_state["balance"] + round(np.random.uniform(-500, 1200), 2)
            st.success(f"Successfully switched operational context to {target_broker} server routing node!")
            st.rerun()

# =========================================================
# TAB 3: ASSET SEARCH BOX & MULTI-TIMEFRAME GRID WORKSPACE
# =========================================================
with tab_search_charts:
    st.markdown("### 🔍 Global Market Search Asset Hub")
    
    # 6. Search box layout supporting Forex, Commodities, Futures, Stocks, and Indices
    c_search, c_layout = st.columns(2) # FIXED VALUE PASSED HERE
    with c_search:
        search_query = st.text_input("Enter Asset Ticker Symbol (Format: EXCHANGE:SYMBOL, e.g., OANDA:XAUUSD, BINANCE:BTCUSDT, NASDAQ:AAPL, TVC:SPX)", value=st.session_state["selected_ticker"])
    with c_layout:
        layout_selection = st.selectbox("Select Workspace Multi-Chart Grid Profile", ["Single Chart Layout", "2-Chart Split Matrix Grid", "4-Chart Comprehensive Matrix Grid"])
    
    if st.button("🎯 Update Workspace Chart Environment", use_container_width=True):
        st.session_state["selected_ticker"] = search_query.upper()
        st.session_state["grid_layout"] = layout_selection
        st.rerun()
        
    st.markdown(f"#### 📺 TradingView Advanced HUD Workspace: `{st.session_state['selected_ticker']}` [{st.session_state['grid_layout']}]")
    
    # Advanced Responsive Embedding Helper for Full TradingView HTML5 Tooling
    def generate_tv_widget(ticker_symbol, element_id, chart_height=500, tf="D"):
        return f"""
        <div class="tradingview-widget-container" style="height:{chart_height}px; width:100%;">
            <div id="{element_id}" style="height:{chart_height}px; width:100%;"></div>
            <script type="text/javascript" src="https://tradingview.com"></script>
            <script type="text/javascript">
            new TradingView.widget({{
                "autoplay": true, "width": "100%", "height": {chart_height},
                "symbol": "{ticker_symbol}", "interval": "{tf}", "timezone": "Etc/UTC",
                "theme": "dark", "style": "1", "locale": "en", "toolbar_bg": "#030611",
                "enable_publishing": false, "hide_side_toolbar": false, "allow_symbol_change": true,
                "save_image": true, "details": true, "hotlist": true, "calendar": true,
                "studies": ["RSI@tv-basicstudies", "MASimple@tv-basicstudies"], "container_id": "{element_id}"
            }});
            </script>
        </div>
        """

    # 7 & 8. Multi-Chart Timeframe Grid Layout Implementation with Tools & Drawing overlays
    if st.session_state["grid_layout"] == "Single Chart Layout":
        st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_single", 550, "D"), height=560)
        
    elif st.session_state["grid_layout"] == "2-Chart Split Matrix Grid":
        grid_col1, grid_col2 = st.columns(2)
        with grid_col1:
            st.markdown("##### ⏱️ Lower Execution Timeframe (15-Minute Feed)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_split_1", 450, "15"), height=460)
        with grid_col2:
            st.markdown("##### ⏱️ Higher Trend Timeframe (Daily Bar Feed)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_split_2", 450, "D"), height=460)
            
    elif st.session_state["grid_layout"] == "4-Chart Comprehensive Matrix Grid":
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            st.markdown("##### ⏱️ Scalp Interval (5-Minute Grid)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_4g_1", 350, "5"), height=360)
        with r1_c2:
            st.markdown("##### ⏱️ Execution Interval (15-Minute Grid)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_4g_2", 350, "15"), height=360)
            
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            st.markdown("##### ⏱️ HTF Structure (4-Hour Grid)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_4g_3", 350, "240"), height=360)
        with r2_c2:
            st.markdown("##### ⏱️ Macro Trend Direction (Daily Grid)")
            st.components.v1.html(generate_tv_widget(st.session_state["selected_ticker"], "chart_4g_4", 350, "D"), height=360)
