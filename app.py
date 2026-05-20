import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

from database.db import (
    init_database,
    add_trade,
    get_trades,
    clear_trades,
)

from core.market_data import get_market_data
from core.smc_engine import detect_malaysian_snr
from core.signal_engine import generate_confluence
from core.risk_engine import calculate_lot_size, risk_lockout
from core.execution_engine import place_mt5_order, EXECUTION_ENABLED

from ui.styles import load_css
from ui.charts import build_chart, build_equity_chart


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="IMMACULATE GOLD PRO",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
init_database()

st_autorefresh(interval=3000, key="auto_refresh")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("⚙️ Control Panel")

    selected_asset = st.selectbox(
        "Asset",
        ["XAUUSD", "BTCUSD", "EURUSD", "US30", "NAS100"]
    )

    timeframe = st.selectbox(
        "Timeframe",
        ["M1", "M5", "M15", "M30", "H1", "H4", "D1"],
        index=2
    )

    live_mode = st.toggle("Use MT5 Live Feed", value=False)

    st.markdown("---")

    risk_amount = st.number_input(
        "Risk Per Trade ($)",
        min_value=10.0,
        value=500.0,
        step=25.0
    )

    stop_distance = st.number_input(
        "Stop Distance",
        min_value=1.0,
        value=20.0,
        step=1.0
    )

    rr = st.number_input(
        "Risk Reward",
        min_value=0.5,
        value=2.0,
        step=0.25
    )

    st.markdown("---")

    max_daily_loss = st.number_input(
        "Max Daily Loss ($)",
        min_value=50.0,
        value=1500.0,
        step=50.0
    )

    max_consecutive_losses = st.number_input(
        "Max Consecutive Losses",
        min_value=1,
        value=3,
        step=1
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <h1 class="green">⚡ IMMACULATE GOLD PRO</h1>
    <p>Institutional automation framework • Malaysian SNR • Daye Quarterly Theory • SMC Confluence Engine</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# CORE DATA
# =========================================================

df, feed_status = get_market_data(
    selected_asset,
    timeframe,
    bars=320,
    live_mode=live_mode
)

trades = get_trades()

snr_zones = detect_malaysian_snr(df)

signal = generate_confluence(df, snr_zones)

locked, lock_reason = risk_lockout(
    trades,
    max_daily_loss,
    max_consecutive_losses
)

price = df["close"].iloc[-1]

lot = calculate_lot_size(
    selected_asset,
    risk_amount,
    stop_distance
)


# =========================================================
# TRADE DIRECTION MODEL
# =========================================================

if signal["bias"].startswith("BULLISH"):
    direction = "BUY"
    entry = price
    sl = price - stop_distance
    tp = price + (stop_distance * rr)

elif signal["bias"].startswith("BEARISH"):
    direction = "SELL"
    entry = price
    sl = price + stop_distance
    tp = price - (stop_distance * rr)

else:
    direction = "WAIT"
    entry = price
    sl = price
    tp = price


# =========================================================
# SIGNAL BADGE
# =========================================================

badge_color = (
    "#052e24"
    if signal["score"] >= 80
    else "#2b2108"
    if signal["score"] >= 60
    else "#310812"
)

badge_border = (
    "#00ffcc"
    if signal["score"] >= 80
    else "#facc15"
    if signal["score"] >= 60
    else "#ff4d6d"
)

st.markdown(
    f"""
    <div class="badge" style="background:{badge_color};border:1px solid {badge_border};">
        {signal['grade']} | SCORE {signal['score']}% | BIAS: {signal['bias']} | ACTION: {direction}
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# METRICS
# =========================================================

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Feed", feed_status)
m2.metric(
    "Live Price",
    f"{price:,.5f}" if selected_asset == "EURUSD" else f"{price:,.2f}"
)
m3.metric("Session", signal["session"])
m4.metric("Daye Phase", signal["quarter"])
m5.metric("Lot Size", lot)

r1, r2, r3, r4 = st.columns(4)

r1.metric("Entry", f"{entry:,.2f}")
r2.metric("Stop Loss", f"{sl:,.2f}")
r3.metric("Take Profit", f"{tp:,.2f}")
r4.metric("Risk Lock", "LOCKED" if locked else "CLEAR")

if locked:
    st.error(f"🛑 Execution blocked: {lock_reason}")
else:
    st.success(f"🟢 Risk engine clear: {lock_reason}")


# =========================================================
# MAIN DASHBOARD
# =========================================================

left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Institutional Chart Engine")
    st.plotly_chart(
        build_chart(df, signal, snr_zones),
        use_container_width=True
    )

with right:
    st.subheader("🧠 Confluence Breakdown")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if signal["reasons"]:
        for reason in signal["reasons"]:
            st.write(f"✅ {reason}")
    else:
        st.write("No strong confluence detected.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🛡️ Execution Engine")

    if direction == "WAIT":
        st.warning("No executable directional bias.")

    elif locked:
        st.error("Risk lockout active.")

    elif signal["score"] < 80:
        st.warning("Execution blocked below 80% confluence.")

    else:
        st.success("Execution conditions met.")

        if st.button("Paper Log Setup", use_container_width=True):
            add_trade(
                asset=selected_asset,
                session=signal["session"],
                quarterly_phase=signal["quarter"],
                bias=signal["bias"],
                setup="Malaysian SNR + Daye Quarterly + SMC",
                confluence_score=int(signal["score"]),
                entry=float(entry),
                stop_loss=float(sl),
                take_profit=float(tp),
                risk_amount=float(risk_amount),
                outcome="PENDING",
                profit=0.0,
                notes="; ".join(signal["reasons"]),
            )

            st.success("Setup logged to database.")
            st.rerun()

        if EXECUTION_ENABLED:
            if st.button("Send MT5 Order", use_container_width=True):
                ok, message = place_mt5_order(
                    selected_asset,
                    direction,
                    lot,
                    sl,
                    tp
                )

                if ok:
                    st.success(message)
                else:
                    st.error(message)


# =========================================================
# EQUITY + LEDGER
# =========================================================

st.subheader("📊 Equity Curve")
st.plotly_chart(
    build_equity_chart(trades),
    use_container_width=True
)

st.subheader("📜 Trade Ledger")

if trades.empty:
    st.info("No trades logged yet.")

else:
    st.dataframe(
        trades,
        use_container_width=True,
        height=260
    )

    csv = trades.to_csv(index=False).encode("utf-8")

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "Download Ledger CSV",
            csv,
            file_name=f"immaculate_gold_ledger_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with c2:
        if st.button("Reset Ledger", use_container_width=True):
            clear_trades()
            st.rerun()


st.caption(
    "Execution is disabled by default. Test everything on demo before enabling MT5 live trading."
)
