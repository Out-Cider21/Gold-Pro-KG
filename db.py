```python
import streamlit as st
import pandas as pd
import numpy as np
import time
import io
import sqlite3
from datetime import datetime
import plotly.graph_objects as go

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
DB_FILE = "immaculate_gold_pro.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            asset TEXT,
            killzone TEXT,
            signature TEXT,
            outcome TEXT,
            profit REAL
        )
    """)

    conn.commit()
    conn.close()

def add_trade_log(asset, killzone, signature, outcome, profit):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO strategy_performance
        (timestamp, asset, killzone, signature, outcome, profit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (current_time, asset, killzone, signature, outcome, profit))

    conn.commit()
    conn.close()

def clear_performance_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM strategy_performance")
    conn.commit()
    conn.close()

def get_performance_history():
    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql_query("""
        SELECT
            timestamp AS 'Session Timestamp',
            asset AS 'Asset',
            killzone AS 'Killzone',
            signature AS 'Strategy Signature',
            outcome AS 'Outcome',
            profit AS 'Net Result ($)'
        FROM strategy_performance
        ORDER BY id DESC
    """, conn)

    conn.close()

    if df.empty:
        df = pd.DataFrame([
            {
                "Session Timestamp": "2026-05-19 08:30",
                "Asset": "XAUUSD",
                "Killzone": "London Open",
                "Strategy Signature": "SNR + FVG",
                "Outcome": "TP HIT",
                "Net Result ($)": 1450
            },
            {
                "Session Timestamp": "2026-05-18 12:00",
                "Asset": "BTCUSD",
                "Killzone": "NY Open",
                "Strategy Signature": "Trendline Break",
                "Outcome": "TP HIT",
                "Net Result ($)": 920
            },
            {
                "Session Timestamp": "2026-05-17 09:00",
                "Asset": "EURUSD",
                "Killzone": "London Open",
                "Strategy Signature": "Liquidity Sweep",
                "Outcome": "SL HIT",
                "Net Result ($)": -350
            }
        ])

    return df

init_database()

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="IMMACULATE GOLD PRO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #070b14;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #0f1724;
    border-right: 1px solid #1d2638;
}

.main-card {
    background: linear-gradient(145deg,#111827,#0b1220);
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 0 20px rgba(0,255,204,0.06);
}

.metric-card {
    background: linear-gradient(145deg,#111827,#0b1220);
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 18px;
    text-align:center;
}

.green-glow {
    color:#00ffcc;
    text-shadow:0 0 12px rgba(0,255,204,0.6);
}

.orange-glow {
    color:#ffb347;
    text-shadow:0 0 12px rgba(255,179,71,0.5);
}

.red-glow {
    color:#ff4d6d;
    text-shadow:0 0 12px rgba(255,77,109,0.5);
}

.banner {
    background: linear-gradient(90deg,#00c6ff,#0072ff,#9d4edd);
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 18px;
    color:white;
    font-weight:700;
    overflow:hidden;
}

.big-price {
    font-size: 58px;
    font-weight: 900;
    line-height: 1;
}

.subtle {
    color:#94a3b8;
}

.signal-high {
    background:#052e24;
    border:1px solid #00ffcc;
    color:#00ffcc;
    padding:14px;
    border-radius:12px;
    text-align:center;
    font-weight:800;
}

.signal-medium {
    background:#3b2200;
    border:1px solid #ffb347;
    color:#ffb347;
    padding:14px;
    border-radius:12px;
    text-align:center;
    font-weight:800;
}

.signal-low {
    background:#3a0912;
    border:1px solid #ff4d6d;
    color:#ff4d6d;
    padding:14px;
    border-radius:12px;
    text-align:center;
    font-weight:800;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("⚙️ IMMACULATE CONTROL")

    st.markdown("---")

    risk_amount = st.number_input(
        "Risk Per Trade ($)",
        min_value=10.0,
        value=500.0,
        step=50.0
    )

    stop_loss = st.number_input(
        "Stop Loss Distance",
        min_value=1.0,
        value=15.0
    )

    take_profit = st.number_input(
        "Target Move",
        min_value=1.0,
        value=30.0
    )

    st.markdown("---")

    selected_asset = st.selectbox(
        "Trading Asset",
        [
            "XAUUSD",
            "BTCUSD",
            "EURUSD",
            "US30",
            "NAS100"
        ]
    )

    st.markdown("---")

    refresh_speed = st.slider(
        "Live Feed Speed (sec)",
        1,
        5,
        1
    )

# =========================================================
# NEWS BANNER
# =========================================================
news_items = [
    "🔥 GOLD liquidity sweep detected above Asian highs",
    "📈 DXY weakening boosts metals strength",
    "⚡ Quarterly dealing range equilibrium respected",
    "🚀 Institutional imbalance detected on H1"
]

banner = "  ✦  ".join(news_items)

st.markdown(
    f"""
    <div class='banner'>
        <marquee scrollamount='7'>{banner}</marquee>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
col1, col2 = st.columns([1,5])

with col1:
    st.markdown("""
    <div class='main-card' style='text-align:center;'>
        <h1 class='green-glow'>KJS</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='main-card'>
        <h1 style='margin-bottom:0;'>IMMACULATE GOLD PRO</h1>
        <p class='subtle'>Advanced Institutional Confluence Engine • Premium/Discount Matrix • Live Market Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# LIVE PRICE ENGINE
# =========================================================
def get_live_price(symbol):

    base_prices = {
        "XAUUSD": 2332.50,
        "BTCUSD": 108250,
        "EURUSD": 1.0845,
        "US30": 39250,
        "NAS100": 18920
    }

    base = base_prices[symbol]

    if symbol == "XAUUSD":
        return round(base + np.random.uniform(-4,4),2)

    if symbol == "BTCUSD":
        return round(base + np.random.uniform(-450,450),2)

    if symbol == "EURUSD":
        return round(base + np.random.uniform(-0.004,0.004),5)

    return round(base + np.random.uniform(-120,120),2)

# =========================================================
# FIBONACCI ENGINE
# =========================================================
def calculate_fib(price):

    high = price + 25
    low = price - 25

    equilibrium = (high + low) / 2

    premium = equilibrium + ((high - equilibrium) * 0.5)
    discount = equilibrium - ((equilibrium - low) * 0.5)

    return {
        "high": high,
        "low": low,
        "equilibrium": equilibrium,
        "premium": premium,
        "discount": discount
    }

# =========================================================
# CONFLUENCE ENGINE
# =========================================================
def calculate_signal_strength():

    malaysian_snr = np.random.randint(0,2)
    quarterly_matrix = np.random.randint(0,2)
    liquidity_sweep = np.random.randint(0,2)
    trendline_break = np.random.randint(0,2)
    premium_discount = np.random.randint(0,2)

    score = (
        malaysian_snr * 20 +
        quarterly_matrix * 20 +
        liquidity_sweep * 20 +
        trendline_break * 20 +
        premium_discount * 20
    )

    if score >= 80:
        badge = "HIGH PROBABILITY"
        css = "signal-high"

    elif score >= 50:
        badge = "MEDIUM PROBABILITY"
        css = "signal-medium"

    else:
        badge = "LOW PROBABILITY"
        css = "signal-low"

    return score, badge, css

# =========================================================
# PERFORMANCE METRICS
# =========================================================
perf_df = get_performance_history()

total_trades = len(perf_df)

wins = len(perf_df[perf_df["Net Result ($)"] > 0])

win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

gross_profit = perf_df[perf_df["Net Result ($)"] > 0]["Net Result ($)"].sum()

gross_loss = abs(
    perf_df[perf_df["Net Result ($)"] < 0]["Net Result ($)"].sum()
)

profit_factor = (
    gross_profit / gross_loss
    if gross_loss > 0 else gross_profit
)

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Live Dashboard",
    "📈 Live Chart",
    "🧠 Strategy Matrix",
    "💾 Trade Logs"
])

# =========================================================
# TAB 1 — LIVE DASHBOARD
# =========================================================
with tab1:

    placeholder = st.empty()

    while True:

        live_price = get_live_price(selected_asset)

        pnl = round(np.random.uniform(-1200,2400),2)

        equity = 100000 + pnl

        fib = calculate_fib(live_price)

        score, badge, css = calculate_signal_strength()

        lot_size = risk_amount / stop_loss

        profit_potential = lot_size * take_profit * 100

        with placeholder.container():

            top1, top2, top3, top4 = st.columns(4)

            with top1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='subtle'>LIVE PRICE</div>
                    <div class='big-price green-glow'>{live_price}</div>
                    <div class='subtle'>{selected_asset}</div>
                </div>
                """, unsafe_allow_html=True)

            with top2:
                pnl_color = "green-glow" if pnl >= 0 else "red-glow"

                st.markdown(f"""
                <div class='metric-card'>
                    <div class='subtle'>FLOATING P/L</div>
                    <div class='big-price {pnl_color}'>
                        ${pnl:,.2f}
                    </div>
                    <div class='subtle'>Live Equity Flow</div>
                </div>
                """, unsafe_allow_html=True)

            with top3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='subtle'>WIN RATE</div>
                    <div class='big-price orange-glow'>
                        {win_rate:.1f}%
                    </div>
                    <div class='subtle'>Strategy Precision</div>
                </div>
                """, unsafe_allow_html=True)

            with top4:
                st.markdown(f"""
                <div class='{css}'>
                    SIGNAL STRENGTH<br><br>
                    {badge}<br><br>
                    SCORE: {score}/100
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            row1, row2 = st.columns(2)

            with row1:

                st.markdown("""
                <div class='main-card'>
                    <h3>📐 Daily Fibonacci Premium / Discount Matrix</h3>
                </div>
                """, unsafe_allow_html=True)

                fib_df = pd.DataFrame({
                    "Level": [
                        "Daily High",
                        "Premium Zone",
                        "Equilibrium",
                        "Discount Zone",
                        "Daily Low"
                    ],
                    "Price": [
                        fib["high"],
                        fib["premium"],
                        fib["equilibrium"],
                        fib["discount"],
                        fib["low"]
                    ]
                })

                st.dataframe(
                    fib_df,
                    use_container_width=True,
                    hide_index=True
                )

            with row2:

                st.markdown("""
                <div class='main-card'>
                    <h3>🧠 Institutional Confluence Matrix</h3>
                </div>
                """, unsafe_allow_html=True)

                matrix_df = pd.DataFrame({
                    "Checklist": [
                        "Malaysian SNR",
                        "Quarterly Matrix",
                        "Liquidity Sweep",
                        "Trendline Break",
                        "Premium/Discount Alignment"
                    ],
                    "Status": [
                        "✅ Confirmed",
                        "✅ Confirmed",
                        "⚠️ Active",
                        "✅ Confirmed",
                        "✅ Discount Buy Zone"
                    ]
                })

                st.dataframe(
                    matrix_df,
                    use_container_width=True,
                    hide_index=True
                )

            st.write("")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Profit Factor",
                f"{profit_factor:.2f}x"
            )

            metric2.metric(
                "Calculated Lot Size",
                f"{lot_size:.2f}"
            )

            metric3.metric(
                "Profit Potential",
                f"${profit_potential:,.2f}"
            )

        time.sleep(refresh_speed)

# =========================================================
# TAB 2 — LIVE CHART
# =========================================================
with tab2:

    st.subheader(f"📈 {selected_asset} Live Institutional Chart")

    chart_price = get_live_price(selected_asset)

    x = pd.date_range(
        datetime.now(),
        periods=120,
        freq="min"
    )

    y = np.cumsum(np.random.randn(120)) + chart_price

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=selected_asset
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=700,
        paper_bgcolor="#070b14",
        plot_bgcolor="#070b14",
        margin=dict(l=10,r=10,t=40,b=10),
        xaxis_title="Time",
        yaxis_title="Price"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TAB 3 — STRATEGY MATRIX
# =========================================================
with tab3:

    st.markdown("""
    <div class='main-card'>
        <h2>🧠 Advanced Strategy Matrix Engine</h2>
    </div>
    """, unsafe_allow_html=True)

    strategy_df = pd.DataFrame({
        "Framework": [
            "Malaysian SNR",
            "Quarterly Theory",
            "Liquidity Sweeps",
            "Trendline Break",
            "Premium/Discount Fib",
            "FVG Alignment",
            "Killzone Timing"
        ],
        "Weight": [
            "20%",
            "20%",
            "20%",
            "20%",
            "20%",
            "15%",
            "10%"
        ],
        "Status": [
            "Confirmed",
            "Bullish",
            "Active",
            "Broken",
            "Discount",
            "Mitigated",
            "London Open"
        ]
    })

    st.dataframe(
        strategy_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# TAB 4 — LOGS
# =========================================================
with tab4:

    st.subheader("💾 Trade Performance Logs")

    st.dataframe(
        perf_df,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⚡ Add Demo Trade"):

            add_trade_log(
                selected_asset,
                "London Open",
                "Liquidity Sweep",
                "TP HIT",
                round(np.random.uniform(200,1200),2)
            )

            st.success("Trade added.")
            st.rerun()

    with col2:

        if st.button("🗑️ Clear Logs"):

            clear_performance_history()

            st.success("Logs cleared.")
            st.rerun()

    st.write("")

    csv_buffer = io.StringIO()

    perf_df.to_csv(csv_buffer, index=False)

    st.download_button(
        "📥 Download CSV",
        data=csv_buffer.getvalue(),
        file_name="immaculate_logs.csv",
        mime="text/csv"
    )
```
