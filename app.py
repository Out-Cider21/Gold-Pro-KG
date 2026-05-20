import streamlit as st
    )

    risk_amount = st.number_input(
        "Risk Per Trade ($)",
        min_value=10.0,
        value=500.0
    )

    stop_loss = st.number_input(
        "Stop Loss Distance",
        min_value=1.0,
        value=15.0
    )

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='main-header'>
<h1>IMMACULATE GOLD PRO</h1>
<p>Institutional Confluence Trading Terminal</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LIVE MARKET DATA
# =====================================================

market_df = get_live_price_data(selected_asset)

current_price = market_df['close'].iloc[-1]

# =====================================================
# MARKET STRUCTURE
# =====================================================

smc_data = detect_market_structure(market_df)

signal_data = generate_signal_score(
    market_df,
    smc_data
)
# =====================================================
# RISK ENGINE
# =====================================================

lot_size, exposure = calculate_lot_size(
    selected_asset,
    risk_amount,
    stop_loss
)

# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("LIVE PRICE", f"{current_price:,.2f}")

with m2:
    st.metric("SIGNAL SCORE", f"{signal_data['score']}%")

with m3:
    st.metric("LOT SIZE", f"{lot_size}")

with m4:
    st.metric("SESSION", get_active_session())

# =====================================================
# SIGNAL ENGINE
# =====================================================

if signal_data['score'] >= 80:
    st.success("HIGH PROBABILITY SETUP DETECTED")
elif signal_data['score'] >= 60:
    st.warning("MEDIUM PROBABILITY SETUP")
else:
    st.error("LOW PROBABILITY ENVIRONMENT")

# =====================================================
# CHARTS
# =====================================================

c1, c2 = st.columns(2)

with c1:
  candlestick_fig = build_candlestick_chart(
        market_df,
        smc_data
    )

    st.plotly_chart(candlestick_fig, use_container_width=True)

with c2:
    trades_df = get_trade_history()

    analytics = calculate_analytics(trades_df)

    equity_fig = build_equity_chart(trades_df)

    st.plotly_chart(equity_fig, use_container_width=True)

# =====================================================
# TRADE HISTORY
# =====================================================

st.subheader("Trade Ledger")
st.dataframe(trades_df, use_container_width=True)
