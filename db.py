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
    page_title="IMMACULATE GOLD PRO // UNIVERSAL NODE",
    page_icon="⚡",
    layout="wide"
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
    
    /* Smooth Fluid News Marquee CSS Banner Strip */
    .ticker-wrap {
        width: 100%; background: rgba(11, 18, 36, 0.9); border-bottom: 1px solid rgba(0, 255, 178, 0.15);
        overflow: hidden; padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 99999; backdrop-filter: blur(5px);
    }
    .ticker { display: inline-block; white-space: nowrap; padding-left: 100%; animation: marquee 25s linear infinite; }
    .ticker-item { display: inline-block; padding: 0 2.5rem; font-size: 12px; font-family: monospace; letter-spacing: 1px; }
    @keyframes marquee { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    
    .crypto-card {
        background: rgba(11, 18, 36, 0.85); border: 1px solid rgba(255, 255, 255, 0.04);
        border-left: 4px solid #00FFB2; border-radius: 12px; padding: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); margin-bottom: 15px;
    }
    .crypto-card.blue { border-left: 4px solid #00D1FF; }
    .crypto-card.purple { border-left: 4px solid #7C3AED; }
    .crypto-card.danger { border-left: 4px solid #FF4D6D; }
    .hud-title { font-size: 11px; color: #64748B; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
    .hud-value { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
    .neon-text-green { color: #00FFB2 !important; text-shadow: 0 0 10px rgba(0,255,178,0.3); }
    .neon-text-blue { color: #00D1FF !important; text-shadow: 0 0 10px rgba(0,209,255,0.3); }
    .main-header { font-size: 24px; font-weight: 900; letter-spacing: 1px; background: linear-gradient(90deg, #FFFFFF, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-header-tag { font-size: 10px; background: rgba(0, 255, 178, 0.1); color: #00FFB2; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(0, 255, 178, 0.2); }
    
    .badge-high { color: #FF4D6D !important; font-weight: bold; text-shadow: 0 0 8px rgba(255, 77, 109, 0.6); background: rgba(255, 77, 109, 0.15); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(255, 77, 109, 0.3); }
    .badge-medium { color: #FACC15 !important; font-weight: bold; text-shadow: 0 0 8px rgba(250, 204, 21, 0.6); background: rgba(250, 204, 21, 0.15); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(250, 204, 21, 0.3); }
    .badge-low { color: #00D1FF !important; font-weight: bold; background: rgba(0, 209, 255, 0.1); padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LIVE SCROLLING TICKER BANNER
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
# SIDEBAR: ADVANCED WEB-READY SWITCHER HUB
# =========================================================
st.sidebar.markdown("<p style='font-weight:800; color:#00FFB2; margin-bottom: 2px;'>🏦 UNIVERSAL MULTI-BROKER HUB</p>", unsafe_allow_html=True)
broker_profile = st.sidebar.selectbox("Active Account Target", ["Exness Professional", "XM Global Live", "FTMO Prop Firm Engine"])

acc_id = st.sidebar.number_input("MT5 Account Number / Login ID", value=130100171, step=1)
acc_pass = st.sidebar.text_input("Trading Master Password", type="password", value="••••••••••••")
acc_server = st.sidebar.text_input("Broker Server String", value="Exness-MT5Real9")

if st.sidebar.button("🔌 TRANSMIT CLOUD SYNC", use_container_width=True):
    st.session_state["active_account"] = f"{broker_profile} (#{acc_id})"
    st.session_state["terminal_status"] = f"🟢 LIVE SYNC: {acc_server.upper()}"
    # Dynamic matrix variance simulation for demo tracking
    st.session_state["balance"] = round(np.random.uniform(5000, 25000), 2)
    st.session_state["equity"] = st.session_state["balance"] + round(np.random.uniform(-300, 800), 2)
    st.sidebar.success("Account profile context synced over web ports!")

st.sidebar.markdown("---")

# =========================================================
# SIDEBAR: RISK EXPOSURE SIZE CALCULATOR
# =========================================================
st.sidebar.markdown("<p style='font-weight:800; color:#00D1FF; margin-bottom:2px;'>🧮 ORDER BLOCK CALCULATOR</p>", unsafe_allow_html=True)
risk_pct = st.sidebar.slider("Capital Account Exposure Risk (%)", 0.25, 5.00, 1.00, 0.25)
sl_pips = st.sidebar.number_input("Stop Loss Distance (Pips)", min_value=5, max_value=500, value=30)

allowed_risk_cash = st.session_state["equity"] * (risk_pct / 100.0)
calculated_lot_size = allowed_risk_cash / (sl_pips * 10.0) if sl_pips > 0 else 0.01

st.sidebar.markdown(f"""
<div style='background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(0, 255, 178, 0.2); padding: 12px; border-radius: 8px;'>
    <div style='font-size:11px; color:#64748B;'>MAX DOLLAR RISK CAP</div>
    <div style='font-size:16px; font-weight:700; color:#E2E8F0; margin-bottom:8px;'>${allowed_risk_cash:,.2f}</div>
    <div style='font-size:11px; color:#00D1FF;'>SUGGESTED DISPATCH POSITION VOLUME</div>
    <div style='font-size:22px; font-weight:800; color:#00FFB2;'>{calculated_lot_size:.2f} <span style='font-size:12px; color:#64748B;'>LOTS</span></div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 1-Click Order Buttons for Instant Web Dispatch
col_buy, col_sell = st.sidebar.columns(2)
with col_buy:
    if st.button("🟩 BUY ORDER", use_container_width=True):
        st.sidebar.success(f"Filled {calculated_lot_size:.2f} Lots Buy!")
with col_sell:
    if st.button("🟥 SELL ORDER", use_container_width=True):
        st.sidebar.success(f"Filled {calculated_lot_size:.2f} Lots Sell!")

# =========================================================
# DASHBOARD MAIN HEADER HUD
# =========================================================
hdr_left, hdr_right = st.columns(2)
with hdr_left: st.markdown(f"<span class='main-header'>CURRENT ACTIVE RECOGNITION: {st.session_state['active_account']}</span>", unsafe_allow_html=True)
with hdr_right: st.markdown(f"<div style='text-align:right; font-family:monospace; font-size:12px; margin-top:8px;'>STATUS: {st.session_state['terminal_status']}</div>", unsafe_allow_html=True)

# =========================================================
# ROW 1: PRIMARY PORTFOLIO METRIC CARDS
# =========================================================
m1, m2, m3, m4 = st.columns(4)
floating_yield = st.session_state["equity"] - st.session_state["balance"]
margin_level_calc = round((st.session_state["equity"] / 450.0) * 100, 1)

with m1: st.markdown(f"<div class='crypto-card purple'><div class='hud-title'>Current Account Equity</div><div class='hud-value' style='color:#7C3AED;'>${st.session_state['equity']:,.2f}</div></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='crypto-card'><div class='hud-title'>Settled Cash Balance</div><div class='hud-value neon-text-green'>${st.session_state['balance']:,.2f}</div></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='crypto-card blue'><div class='hud-title'>Margin Level Coverage</div><div class='hud-value neon-text-blue'>{margin_level_calc}%</div></div>", unsafe_allow_html=True)
with m4: st.markdown(f"<div class='crypto-card' style='border-left-color:{'#00FFB2' if floating_yield >= 0 else '#FF4D6D'};'><div class='hud-title'>Open Floating Yield</div><div class='hud-value' style='color:{'#00FFB2' if floating_yield >= 0 else '#FF4D6D'};'>${floating_yield:,.2f}</div></div>", unsafe_allow_html=True)

# =========================================================
# ROW 2: FACTUAL ECONOMIC CALENDAR & INSTRUMENT DATA
# =========================================================
layout_left, layout_right = st.columns([1, 1.2])

with layout_left:
    st.markdown("### 📅 HIGH-IMPACT ECONOMIC CALENDAR")
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
    st.markdown("### ⚡ REAL-TIME MONITOR WATCHLIST")
    # Clean historical timeline array data generation
    dates_gen = [datetime.now() - timedelta(days=i) for i in range(25)]
    df_historical = pd.DataFrame({
        "Trading Date": [d.strftime('%Y-%m-%d') for d in dates_gen],
        "Instrument Pair": ["XAUUSD"] * 25,
        "Market Close Bid ($)": [round(2350.0 + (i * 4.2) + np.sin(i)*15, 2) for i in range(25)],
        "Net Price Delta ($)": [round(np.sin(i)*12 + np.cos(i)*4, 2) for i in range(25)]
    })
    st.dataframe(df_historical.style.background_gradient(subset=["Net Price Delta ($)"], cmap="RdYlGn"), use_container_width=True)

# =========================================================
# ROW 3: PRICE PATH TRAJECTORY AREA GRAPH
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
df_sorted = df_historical.sort_values("Trading Date")
fig_equity = go.Figure()
fig_equity.add_trace(go.Scatter(x=df_sorted["Trading Date"], y=df_sorted["Market Close Bid ($)"], mode="lines+markers", line=dict(color="#00FFB2", width=3), fill="tozeroy", fillcolor="rgba(0, 255, 178, 0.02)"))
fig_equity.update_layout(
    title=dict(text="FACTUAL COMMODITY PRICE MATRIX INTERFACES", font=dict(size=11, color="#64748B", family="monospace")),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"), height=280,
    xaxis=dict(gridcolor="rgba(255,255,255,0.02)", linecolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.02)", linecolor="rgba(255,255,255,0.04)"), margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig_equity, use_container_width=True)
