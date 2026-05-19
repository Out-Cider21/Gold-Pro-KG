import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="IMMACULATE GOLD PRO // TRADING NODE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "active_account": "FTMO Prop Client (#1513449340)",
    "terminal_status": "🟢 SYNC TO FTMO-DEMO",
    "balance": 100000.50,
    "equity": 100000.50,
    "free_margin": 100000.50,
    "margin_level": 0.0,
    "selected_ticker": "XAUUSD",
    "grid_layout": "Single Chart Layout"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# PREMIUM CSS
# =========================================================
st.markdown("""
<style>

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    background-color: #030611 !important;
    color: #E2E8F0 !important;
    font-family: 'SF Pro Display', sans-serif;
}

/* HEADER */
.main-header {
    font-size: 28px;
    font-weight: 900;
    color: white;
}

/* CARDS */
.crypto-card {
    background: rgba(11,18,36,0.88);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
    border-left: 4px solid #00FFB2;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

.crypto-card.blue {
    border-left: 4px solid #00D1FF;
}

.crypto-card.purple {
    border-left: 4px solid #7C3AED;
}

.crypto-card.warning {
    border-left: 4px solid #FACC15;
}

.crypto-card.danger {
    border-left: 4px solid #FF4D6D;
}

.crypto-card.ai {
    border-left: 4px solid #A855F7;
}

.hud-title {
    color: #64748B;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.hud-value {
    font-size: 26px;
    font-weight: 900;
}

.green {
    color: #00FFB2;
}

.red {
    color: #FF4D6D;
}

.blue {
    color: #00D1FF;
}

.purple {
    color: #A855F7;
}

.yellow {
    color: #FACC15;
}

/* NEWS TICKER */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: rgba(11,18,36,0.95);
    border-bottom: 1px solid rgba(0,255,178,0.15);
    padding: 10px 0;
    margin-bottom: 20px;
}

.ticker {
    display: inline-block;
    white-space: nowrap;
    animation: tickerMove 35s linear infinite;
}

.ticker-item {
    display: inline-block;
    padding-right: 60px;
    font-size: 13px;
    font-weight: bold;
}

@keyframes tickerMove {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# NEWS BANNER
# =========================================================
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        <span class="ticker-item" style="color:#00FFB2;">
            🔥 XAUUSD MARKET FEED: Gold Approaching Key Resistance Levels
        </span>

        <span class="ticker-item" style="color:#00D1FF;">
            ⚡ FED WATCH: Traders Pricing Lower Rate Cuts
        </span>

        <span class="ticker-item" style="color:#FF4D6D;">
            ⚠️ VOLATILITY ALERT: US Session Expected To Expand Range
        </span>

        <span class="ticker-item" style="color:#FACC15;">
            📊 GOLD TARGETS: Institutional Desks Watching $5000 Long Term
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## 🧮 Position Calculator")

risk_cash_input = st.sidebar.number_input(
    "Risk Amount ($)",
    min_value=1.0,
    value=500.0,
    step=50.0
)

sl_distance_usd = st.sidebar.number_input(
    "Stop Loss Distance ($)",
    min_value=0.1,
    value=10.0,
    step=0.5
)

tp_distance_usd = st.sidebar.number_input(
    "Take Profit Distance ($)",
    min_value=0.1,
    value=20.0,
    step=1.0
)

calculated_lots = risk_cash_input / sl_distance_usd
profit_potential = calculated_lots * tp_distance_usd * 100

st.sidebar.markdown(f"""
<div class="crypto-card">
    <div class="hud-title">Suggested Lots</div>
    <div class="hud-value green">{calculated_lots:.2f}</div>

    <div class="hud-title" style="margin-top:15px;">Profit Potential</div>
    <div class="hud-value blue">${profit_potential:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🏦 Account Manager",
    "📺 Live Charts"
])

# =========================================================
# TAB 1 - DASHBOARD
# =========================================================
with tab1:

    left, right = st.columns([3,1])

    with left:
        st.markdown(
            f"<div class='main-header'>{st.session_state['active_account']}</div>",
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            f"<div style='text-align:right; margin-top:15px;'>{st.session_state['terminal_status']}</div>",
            unsafe_allow_html=True
        )

    floating = st.session_state["equity"] - st.session_state["balance"]

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        color = "red" if floating < 0 else "green"

        st.markdown(f"""
        <div class="crypto-card danger">
            <div class="hud-title">Floating P/L</div>
            <div class="hud-value {color}">
                ${floating:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="crypto-card purple">
            <div class="hud-title">Equity</div>
            <div class="hud-value purple">
                ${st.session_state['equity']:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="crypto-card">
            <div class="hud-title">Balance</div>
            <div class="hud-value green">
                ${st.session_state['balance']:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="crypto-card blue">
            <div class="hud-title">Free Margin</div>
            <div class="hud-value blue">
                ${st.session_state['free_margin']:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="crypto-card warning">
            <div class="hud-title">Margin Level</div>
            <div class="hud-value yellow">
                {st.session_state['margin_level']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # AI PANELS
    # =====================================================
    st.markdown("## 🧠 AI Market Engine")

    a1, a2, a3 = st.columns(3)

    with a1:
        st.markdown("""
        <div class="crypto-card ai">
            <div class="hud-title">AI Bias</div>
            <div class="hud-value purple">
                STRONG BULLISH
            </div>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="crypto-card ai">
            <div class="hud-title">Volatility</div>
            <div class="hud-value green">
                LOW REVERSAL
            </div>
        </div>
        """, unsafe_allow_html=True)

    with a3:
        st.markdown("""
        <div class="crypto-card ai">
            <div class="hud-title">Liquidity Target</div>
            <div class="hud-value blue">
                2368.50
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # CHART
    # =====================================================
    st.markdown("## 📈 Commodity Matrix")

    dates = [datetime.now() - timedelta(days=i) for i in range(15)]

    prices = [2350 + i * 4 for i in range(15)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode="lines+markers",
        fill="tozeroy"
    ))

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 2 - ACCOUNT MANAGER
# =========================================================
with tab2:

    st.markdown("## 🏦 Account Management")

    broker = st.selectbox(
        "Broker",
        [
            "FTMO",
            "Exness",
            "XM",
            "IC Markets"
        ]
    )

    account_id = st.number_input(
        "Account Number",
        value=1513449340
    )

    balance = st.number_input(
        "Balance",
        value=100000.50
    )

    equity = st.number_input(
        "Equity",
        value=100000.50
    )

    free_margin = st.number_input(
        "Free Margin",
        value=100000.50
    )

    server = st.text_input(
        "Server",
        value="FTMO-Demo"
    )

    if st.button("🔌 Sync Account"):

        used_margin = max(equity - free_margin, 1)
        margin_level = (equity / used_margin) * 100

        st.session_state["active_account"] = f"{broker} (#{account_id})"
        st.session_state["terminal_status"] = f"🟢 SYNC TO {server.upper()}"
        st.session_state["balance"] = balance
        st.session_state["equity"] = equity
        st.session_state["free_margin"] = free_margin
        st.session_state["margin_level"] = margin_level

        st.success("Account synced successfully.")

# =========================================================
# TRADINGVIEW FUNCTION
# =========================================================
def create_tradingview_widget(symbol="OANDA:XAUUSD", interval="15"):

    html_code = f"""
    <div class="tradingview-widget-container">
        <div id="tradingview_chart"></div>

        <script
            type="text/javascript"
            src="https://s3.tradingview.com/tv.js">
        </script>

        <script type="text/javascript">

        new TradingView.widget(
        {{
            "autosize": true,
            "symbol": "{symbol}",
            "interval": "{interval}",
            "timezone": "Africa/Johannesburg",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#030611",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_chart"
        }});

        </script>
    </div>
    """

    return html_code

# =========================================================
# TAB 3 - LIVE CHARTS
# =========================================================
with tab3:

    st.markdown("## 📺 Live TradingView Charts")

    col1, col2 = st.columns(2)

    with col1:
        search_query = st.text_input(
            "Ticker Symbol",
            value=st.session_state["selected_ticker"]
        )

    with col2:
        layout_selection = st.selectbox(
            "Chart Layout",
            [
                "Single Chart Layout",
                "2-Chart Split Matrix Grid",
                "4-Chart Comprehensive Matrix Grid"
            ]
        )

    if st.button("🎯 Load Live Charts"):

        st.session_state["selected_ticker"] = search_query.upper()
        st.session_state["grid_layout"] = layout_selection

    ticker = st.session_state["selected_ticker"]

    # =====================================================
    # AUTO SYMBOL MAPPING
    # =====================================================
    if ":" not in ticker:

        if ticker in ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]:
            ticker = f"OANDA:{ticker}"

        elif ticker in ["BTCUSDT", "ETHUSDT"]:
            ticker = f"BINANCE:{ticker}"

        elif ticker in ["NAS100", "US30", "SPX500"]:
            ticker = f"TVC:{ticker}"

        else:
            ticker = f"TVC:{ticker}"

    st.markdown(f"### 🔥 {ticker}")

    # =====================================================
    # SINGLE CHART
    # =====================================================
    if st.session_state["grid_layout"] == "Single Chart Layout":

        st.components.v1.html(
            create_tradingview_widget(ticker, "15"),
            height=700
        )

    # =====================================================
    # 2 CHART LAYOUT
    # =====================================================
    elif st.session_state["grid_layout"] == "2-Chart Split Matrix Grid":

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("#### 15 Minute")

            st.components.v1.html(
                create_tradingview_widget(ticker, "15"),
                height=600
            )

        with c2:

            st.markdown("#### Daily")

            st.components.v1.html(
                create_tradingview_widget(ticker, "D"),
                height=600
            )

    # =====================================================
    # 4 CHART GRID
    # =====================================================
    elif st.session_state["grid_layout"] == "4-Chart Comprehensive Matrix Grid":

        r1c1, r1c2 = st.columns(2)

        with r1c1:

            st.markdown("#### 5 Minute")

            st.components.v1.html(
                create_tradingview_widget(ticker, "5"),
                height=500
            )

        with r1c2:

            st.markdown("#### 15 Minute")

            st.components.v1.html(
                create_tradingview_widget(ticker, "15"),
                height=500
            )

        r2c1, r2c2 = st.columns(2)

        with r2c1:

            st.markdown("#### 4 Hour")

            st.components.v1.html(
                create_tradingview_widget(ticker, "240"),
                height=500
            )

        with r2c2:

            st.markdown("#### Daily")

            st.components.v1.html(
                create_tradingview_widget(ticker, "D"),
                height=500
            )
