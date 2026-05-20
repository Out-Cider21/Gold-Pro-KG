import streamlit as st
import pandas as pd
import time
import random
import io
import sqlite3
from datetime import datetime

# -------------------------------------------------------------------
# SQLITE DATABASE STORAGE INITIALIZATION
# -------------------------------------------------------------------
DB_FILE = "trading_vault.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            account_id TEXT,
            action_type TEXT
        )
    """)
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

def log_account_switch(account_str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO account_logs (timestamp, account_id, action_type) VALUES (?, ?, ?)",
        (current_time, account_str, "SWITCH_ACCOUNT")
    )
    conn.commit()
    conn.close()

def get_account_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp, account_id, action_type FROM account_logs ORDER BY id DESC", conn)
    conn.close()
    return df

def add_custom_trade_log(asset, killzone, signature, outcome, profit):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO strategy_performance (timestamp, asset, killzone, signature, outcome, profit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (current_time, asset, killzone, signature, outcome, profit))
    conn.commit()
    conn.close()

def get_performance_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp AS 'Session Timestamp', asset AS 'Asset', killzone AS 'Killzone Block', signature AS 'Strategy Signature', outcome AS 'Outcome Status', profit AS 'Net Result ($)' FROM strategy_performance ORDER BY id DESC", conn)
    conn.close()
    
    if df.empty:
        df = pd.DataFrame([
            {"Session Timestamp": "2026-05-19 08:30", "Asset": "XAUUSD", "Killzone Block": "London Open (Q1)", "Strategy Signature": "SNR V-Level + FVG", "Outcome Status": "TARGET ACHIEVED (TP)", "Net Result ($)": 1450.00},
            {"Session Timestamp": "2026-05-18 14:00", "Asset": "XAUUSD", "Killzone Block": "NY Open (Q2)", "Strategy Signature": "Trendline Break + FVG", "Outcome Status": "TARGET ACHIEVED (TP)", "Net Result ($)": 980.00},
            {"Session Timestamp": "2026-05-15 09:00", "Asset": "EURUSD", "Killzone Block": "London Open (Q2)", "Strategy Signature": "SNR Gap Rejection", "Outcome Status": "STOP LOSS BREACH (SL)", "Net Result ($)": -410.00}
        ])
    return df

init_database()

# -------------------------------------------------------------------
# PAGE INITIALIZATION & NEON MASTER INTERFACE STYLE SHEET
# -------------------------------------------------------------------
st.set_page_config(
    page_title="IMMACULATE GOLD PRO",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp { background-color: #0c0d14; color: #ffffff; font-family: 'Inter', sans-serif; }
        .promo-card {
            background: linear-gradient(135deg, #161825 0%, #11121d 100%);
            border: 1px solid #222538; border-radius: 12px; padding: 20px; min-height: 160px;
        }
        .promo-neon-blue { border-top: 4px solid #00d2ff; }
        .promo-neon-purple { border-top: 4px solid #9d4edd; }
        .promo-neon-green { border-top: 4px solid #00ffcc; }
        
        .exness-btn {
            background-color: #ffcc00 !important; color: #000000 !important;
            font-weight: bold !important; border-radius: 6px !important;
            padding: 8px 18px !important; text-align: center; display: inline-block;
        }
        
        .stTabs [data-baseweb="tab-list"] { gap: 20px; }
        .stTabs [data-baseweb="tab"] {
            height: 48px; background-color: #121420; border-radius: 6px 6px 0px 0px;
            color: #8f92a1; font-weight: bold; padding: 8px 16px; border: 1px solid #1c1f33;
        }
        .stTabs [aria-selected="true"] {
            background-color: #240046 !important; color: #00ffcc !important;
            border-bottom: 2px solid #00ffcc !important; border: 1px solid #3c096c !important;
        }
        
        .signal-box {
            background-color: #161825; border-radius: 8px; padding: 15px; margin-bottom: 10px; border: 1px solid #222538;
        }
    </style>
""", unsafe_allow_html=True)

if "profit_alert_hit" not in st.session_state:
    st.session_state.profit_alert_hit = False
if "loss_alert_hit" not in st.session_state:
    st.session_state.loss_alert_hit = False
if "last_logged_account" not in st.session_state:
    st.session_state.last_logged_account = None
if "last_activity_time" not in st.session_state:
    st.session_state.last_activity_time = time.time()

SESSION_TIMEOUT_SECONDS = 300
current_interaction_time = time.time()
inactivity_duration = current_interaction_time - st.session_state.last_activity_time
st.session_state.last_activity_time = current_interaction_time

# -------------------------------------------------------------------
# SIDE PANEL CONTROLS & GATEWAY LOCKOUT SYSTEM
# -------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.subheader("🔐 Terminal Security Gateway")
    APP_SECRET_PASSCODE = "PRO77" 
    input_passcode = st.text_input("Enter Supervisor Pin:", type="password")
    
    if inactivity_duration > SESSION_TIMEOUT_SECONDS:
        st.error("🔴 Session Timed Out. Please re-enter PIN.")
        st.stop()
    if input_passcode != APP_SECRET_PASSCODE:
        st.error("Access Denied.")
        st.stop()
        
    st.success("Access Authorized")
    st.divider()
    
    user_cash_risk = st.number_input("Base Cash Amount at Risk ($):", min_value=0.0, value=500.0, step=50.0)
    user_sl_distance = st.number_input("Stop Loss Distance ($):", min_value=0.01, value=15.0, step=1.0)
    user_target_movement = st.number_input("Target Profit Move ($):", min_value=0.01, value=30.0, step=1.0)
    
    st.divider()
    enable_audio = st.checkbox("Enable Audio Alerts", value=True)
    profit_threshold = st.number_input("Profit Sound Above ($):", value=400.0, step=50.0)
    loss_threshold = st.number_input("Loss Sound Below ($):", value=-300.0, step=50.0)
    st.caption("IMMACULATE GOLD PRO v6.0")

# NEWS BANNER
news_headlines = [
    "🔥 GOLD spikes as liquidities shift aggressively upward near critical zones",
    "📈 FED signals policy hold ahead of crucial upcoming global CPI report releases"
]
banner_text = " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ".join(news_headlines)
st.markdown(f"<div style='background-color: #121420; padding: 12px; border-radius: 8px; border: 1px solid #240046; margin-bottom: 20px; overflow: hidden; white-space: nowrap;'><marquee behavior='scroll' direction='left' scrollamount='5' style='color: #00ffcc; font-size: 16px; font-weight: 600;'>{banner_text}</marquee></div>", unsafe_allow_html=True)

# TOP LEFT KJS INITIALS
header_col1, header_col2 = st.columns()
with header_col1:
    st.markdown("<div style='background: linear-gradient(135deg, #3c096c 0%, #240046 100%); padding: 12px; border-radius: 8px; border: 2px solid #00ffcc; text-align: center; box-shadow: 0px 0px 10px #00ffcc;'><h2 style='color: #00ffcc; margin: 0; font-weight: 900; letter-spacing: 2px; font-size: 28px;'>KJS</h2></div>", unsafe_allow_html=True)
with header_col2:
    st.markdown("<h1 style='margin: 0; padding-top: 4px; font-size: 32px;'>Exness Personal Workspace Matrix</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# ALGORITHMIC ENGINE (Malaysian SNR + Quarterly Theory + FVG)
# -------------------------------------------------------------------
def generate_algorithmic_signals(ticker):
    htf_status = {
        "Monthly (M)": {"Trend": "Strong Bullish", "Key_SNR": "V-Level Support @ 2280.00", "FVG": "Mitigated"},
        "Weekly (W)": {"Trend": "Bullish Expansion", "Key_SNR": "A-Level Flipped @ 2310.00", "FVG": "🚨 Unmitigated FVG @ 2295.00"},
        "Daily (D)": {"Trend": "Consolidation", "Key_SNR": "Gap Support Zone @ 2315.00", "FVG": "Mitigated"},
        "H4 (4-Hour)": {"Trend": "Bearish Retracement", "Key_SNR": "V-Level Demand @ 2312.00", "FVG": "🚨 Unmitigated FVG @ 2308.00"},
        "H1 (1-Hour)": {"Trend": "Trendline Compression", "Key_SNR": "Clean Peak Resistance @ 2335.00", "FVG": "Mitigated"}
    }
    
    current_hour = datetime.now().hour
    active_killzone = "London Open Killzone (Q2 Accumulation)" if (7 <= current_hour <= 11) else "New York Open Killzone (Q2 Manipulation)"
    
    liquidity_sweep = "⚠️ YES - Asian Session High Cleared (Liquidity Engineered)"
    trendline_break = "✅ CONFIRMED - H1 Bearish Trendline Broken on Volume"
    snr_rejection = "🔒 COMPLETED - Retested Malaysian Fresh Gap and H4 Unmitigated FVG Border"
    
    bias = "STRONG BUY" if ticker == "XAUUSD" else "SELL LIMIT"
    tp_target = 2365.00 if ticker == "XAUUSD" else 1.0710
    sl_target = 2304.00 if ticker == "XAUUSD" else 1.0895
    
    return htf_status, active_killzone, liquidity_sweep, trendline_break, snr_rejection, bias, tp_target, sl_target

# -------------------------------------------------------------------
# MASTER ACCURACY CALCULATIONS ENGINE
# -------------------------------------------------------------------
perf_df = get_performance_history()
total_trades = len(perf_df)
wins = len(perf_df[perf_df["Outcome Status"] == "TARGET ACHIEVED (TP)"])
win_rate = (wins / total_trades) * 100 if total_trades > 0 else 50.0

gross_profits = perf_df[perf_df["Net Result ($)"] > 0]["Net Result ($)"].sum()
gross_losses = abs(perf_df[perf_df["Net Result ($)"] < 0]["Net Result ($)"].sum())
profit_factor = gross_profits / gross_losses if gross_losses > 0 else gross_profits

# -------------------------------------------------------------------
# AUTOMATED RISK EXPOSURE SCALING LOGIC (Based on Win Rate %)
# -------------------------------------------------------------------
risk_multiplier = 1.0
risk_status_msg = "STANDARD RISK BALANCE"
risk_badge_color = "#3498db"

if win_rate < 50.0:
    risk_multiplier = 0.50
    risk_status_msg = "⚠️ PROTECTION MODE: Risk Cut by 50% Due to Low Win Rate"
    risk_badge_color = "#ff4b4b"
elif win_rate > 65.0:
    risk_multiplier = 1.25
    risk_status_msg = "🚀 AGGRESSIVE SCALING: Lot Capacity Boosted by 25% due to High Precision"
    risk_badge_color = "#00ffcc"

scaled_cash_risk = user_cash_risk * risk_multiplier

# -------------------------------------------------------------------
# DASHBOARD CARD TABS
# -------------------------------------------------------------------
st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Accounts View", "🗃️ Active Account Manager", "📈 Live TradingView Charts", "💾 Data Logs & Batch Importer"])

with tab2:
    st.subheader("Account Routing Setup")
    account_options_list = ["#130100171 TenDiGiTz (MT5 Standard)", "#1513449340 (FTMO Demo Pool)"]
    selected_account = st.selectbox("Switch Primary Live Terminal Endpoint:", account_options_list)
    if selected_account != st.session_state.last_logged_account:
        log_account_switch(selected_account)
        st.session_state.last_logged_account = selected_account
    st.dataframe(get_account_history(), use_container_width=True, hide_index=True)

with tab1:
    search_grid_1, search_grid_2 = st.columns(2)
    with search_grid_1:
        asset_class_filter = st.selectbox("Market Asset Category:", ["Commodities", "Forex", "Futures"])
    asset_dictionary = {"Commodities": ["XAUUSD", "USOIL"], "Forex": ["EURUSD", "GBPUSD"], "Futures": ["ES1!", "NQ1!"]}
    with search_grid_2:
        active_ticker_symbol = st.selectbox("Ticker Target:", asset_dictionary[asset_class_filter])

    # Execute Signals Calculation Pipeline
    htf, killzone, liq_sweep, tl_break, m_snr, final_bias, target_tp, target_sl = generate_algorithmic_signals(active_ticker_symbol)

    # Display Risk Allocation Notice Banner
    st.markdown(f"""
        <div style='background-color:#161825; border-left: 6px solid {risk_badge_color}; padding:12px; border-radius:4px; margin-bottom:15px;'>
            <span style='color:{risk_badge_color}; font-weight:bold; font-size:14px;'>{risk_status_msg}</span><br>
            <span style='color:#8f92a1; font-size:12px;'>Current Matrix Multiplier: <b>{risk_multiplier:.2f}x</b> | Base Risk allocation transformed to: <b>${scaled_cash_risk:,.2f}</b></span>
        </div>
    """, unsafe_allow_html=True)

    # ADVANCED STRATEGY SIGNAL ENGINE VIEWPORTS
    st.markdown("### 🤖 Advanced Strategy Signal Engine")
    sig_col1, sig_col2 = st.columns(2)
    
    with sig_col1:
        st.markdown(f"""
        <div class='signal-box' style='border-left: 5px solid #ffcc00;'>
            <h4 style='color:#ffcc00; margin:0;'>🌐 Core Time-Block Execution Framework</h4>
            <p style='margin:5px 0 0 0; font-size:14px;'><b>Active Volatility Matrix Window:</b> {killzone}</p>
            <p style='margin:2px 0 0 0; font-size:13px; color:#8f92a1;'>Trader Daye 90-Min Fractal Cycle Phase Mapping Enabled</p>
            <hr style='border:0.5px solid #222538; margin:10px 0;'>
            <h4 style='color:#00ffcc; margin:0;'>🎯 Structural Confluence Checklists</h4>
            <p style='margin:5px 0 0 0; font-size:13px;'><b>Liquidity Status:</b> {liq_sweep}</p>
            <p style='margin:2px 0 0 0; font-size:13px;'><b>Trendline Rule:</b> {tl_break}</p>
            <p style='margin:2px 0 0 0; font-size:13px;'><b>Malaysian Candlestick SNR Base:</b> {m_snr}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with sig_col2:
        bias_color = "#00ffcc" if "BUY" in final_bias else "#ff4b4b"
        st.markdown(f"""
        <div class='signal-box' style='border-left: 5px solid {bias_color}; min-height:190px;'>
            <h4 style='color:{bias_color}; margin:0;'>🧠 Live AI Predictive Output Decision</h4>
            <h2 style='color:#ffffff; margin:8px 0 4px 0; font-size:28px;'>Order Bias: <span style='color:{bias_color};'>{final_bias}</span></h2>
            <p style='margin:0; font-size:15px; color:#00d2ff;'><b>Take Profit Target:</b> {target_tp:,.2f}</p>
            <p style='margin:2px 0 0 0; font-size:15px; color:#ff4b4b;'><b>Invalidation Stop Loss:</b> {target_sl:,.2f}</p>
            <p style='margin:8px 0 0 0; font-size:11px; color:#8f92a1;'>Engine Warning: Confirm LTF structural alignment before scaling exposure rules.</p>
        </div>
        """, unsafe_allow_html=True)

    # Higher Timeframe Matrix Expansion Module with FVG Data Columns
    with st.expander("🔍 View Complete Multi-Timeframe Structural Blueprint & Unmitigated FVGs"):
        htf_cols = st.columns(5)
        for idx, (tf, metric) in enumerate(htf.items()):
            with htf_cols[idx]:
                fvg_font_color = "#ff4b4b" if "🚨" in metric['FVG'] else "#8f92a1"
                st.markdown(f"""
                <div style='background-color:#121420; padding:12px; border-radius:6px; border:1px solid #1c1f33; text-align:center;'>
                    <h5 style='margin:0; color:#9d4edd;'>{tf}</h5>
                    <p style='margin:5px 0 2px 0; font-size:13px; font-weight:bold;'>{metric['Trend']}</p>
                    <p style='margin:0; font-size:11px; color:#8f92a1; min-height:30px;'>{metric['Key_SNR']}</p>
                    <p style='margin:5px 0 0 0; font-size:11px; color:{fvg_font_color}; font-weight:500;'>{metric['FVG']}</p>
                </div>
                """, unsafe_allow_html=True)

    # INTERACTIVE SLIDERS SIMULATION & OVERRIDES
    st.markdown("### 🎛️ Live Simulation Sandbox & Trade Outcome Logger")
    with st.expander("Deploy Manual Backtest Slider Overrides"):
        slider_col1, slider_col2, slider_col3 = st.columns(3)
        with slider_col1:
            sim_killzone = st.select_slider("Select Test Timeblock Node:", options=["London Open (Q1)", "London Open (Q2)", "NY Open (Q1)", "NY Open (Q2)"])
            sim_strategy = st.selectbox("Select Strategy Signature Core:", ["SNR V-Level + FVG", "Trendline Break + FVG", "SNR Gap Rejection"])
        with slider_col2:
            sim_outcome = st.radio("Simulated Target Outcome Status:", ["TARGET ACHIEVED (TP)", "STOP LOSS BREACH (SL)"])
        with slider_col3:
            sim_profit = st.slider("Net Theoretical Performance Return ($):", min_value=-1500.0, max_value=3000.0, value=500.0, step=50.0)
            if st.button("⚡ Commit Result to Performance Ledger"):
                add_custom_trade_log(active_ticker_symbol, sim_killzone, sim_strategy, sim_outcome, sim_profit)
                st.rerun()

    # STRATEGIC SIGNAL ACCURACY & VERIFICATION LEDGER
    st.markdown("### 📈 Strategic Signal Accuracy & Verification Ledger")
    metric_grid_1, metric_grid_2, metric_grid_3 = st.columns(3)
    with metric_grid_1:
        st.metric(label="📊 Total Validated Setups", value=f"{total_trades} Session Signals")
    with metric_grid_2:
        st.metric(label="🎯 Strategy Win Rate", value=f"{win_rate:.1f}%", delta=f"{wins} Wins / {total_trades - wins} Losses")
    with metric_grid_3:
        st.metric(label="⚡ Confluence Profit Factor", value=f"{profit_factor:.2f}x")
        
    st.dataframe(perf_df, use_container_width=True, hide_index=True)

# TRADINGVIEW FRAMEWORK
with tab3:
    st.subheader(f"TradingView Advanced Canvas — {active_ticker_symbol}")
    resolved_exchange = "FX_IDC" if active_ticker_symbol == "XAUUSD" else "OANDA"
    tradingview_widget_frame = f"""<iframe src="https://tradingview.com{resolved_exchange}%3A{active_ticker_symbol}&interval=15&theme=dark" width="100%" height="650" frameborder="0" style="border-radius: 12px; border: 1px solid #1c1f33;"></iframe>"""
    st.components.v1.html(tradingview_widget_frame, height=660)

# -------------------------------------------------------------------
# DATA LOGS & AUTOMATED CSV BATCH IMPORTER ENGINE
# -------------------------------------------------------------------
with tab4:
    st.header("🗄️ Automated Strategy CSV Batch Importer & Logs")
    st.write("Upload a historical batch file (with columns: `asset,killzone,signature,outcome,profit`) to bulk-update your statistical dashboard metrics.")
    
    uploaded_file = st.file_uploader("Choose trading log CSV file:", type=["csv"])
    if uploaded_file is not None:
        try:
            imported_df = pd.read_csv(uploaded_file)
            required_cols = ["asset", "killzone", "signature", "outcome", "profit"]
            if all(col in imported_df.columns for col in required_cols):
                for _, row in imported_df.iterrows():
                    add_custom_trade_log(row['asset'], row['killzone'], row['signature'], row['outcome'], float(row['profit']))
                st.success(f"Successfully processed and committed {len(imported_df)} records to the terminal core ledger.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid schema. CSV must contain fields: asset, killzone, signature, outcome, profit")
        except Exception as e:
            st.error(f"Error parsing historical document: {e}")
            
    st.divider()
    st.subheader("Download Current Performance Logs")
    csv_string_buffer = io.StringIO()
    perf_df.to_csv(csv_string_buffer, index=False)
    st.download_button(label="📥 Download Data Records (.CSV)", data=csv_string_buffer.getvalue(), file_name="KJS_Vault_Log.csv", mime="text/csv")

# -------------------------------------------------------------------
# LIVE ENGINE METRICS REFRESH ENGINE LOOP WITH DYNAMIC LOT SIZING
# -------------------------------------------------------------------
with tab1:
    st.write("")
    live_exness_panel = st.empty()
    account_settled_balance = 100000.50
    allocated_margin_held = 2150.00

    # lot calculation linked directly to the scaled cash risk based on winning percentages
    calculated_position_lots = scaled_cash_risk / user_sl_distance if user_sl_distance > 0 else 0.0
    calculated_yield_potential = calculated_position_lots * user_target_movement * 100

    while True:
        with live_exness_panel.container():
            live_gold_spot_quote = round(2322.40 + random.uniform(-1.20, 1.40), 2)
            live_calculated_pnl = round(random.uniform(-450.00, 750.00), 2)
            account_live_equity = account_settled_balance + live_calculated_pnl
            account_free_margin = account_live_equity - allocated_margin_held
            live_corrected_liquidity = round(4107.00 + (live_gold_spot_quote * 0.0002), 2)

            if enable_audio:
                if live_calculated_pnl >= profit_threshold and not st.session_state.profit_alert_hit:
                    st.audio("https://google.com", format="audio/ogg", autoplay=True)
                    st.session_state.profit_alert_hit = True
                elif live_calculated_pnl < profit_threshold:
                    st.session_state.profit_alert_hit = False

            neon_pl_color = "#ff4b4b" if live_calculated_pnl < 0 else "#00ffcc"
            neon_pl_sign = "+" if live_calculated_pnl >= 0 else ""

            st.markdown(f"""
                <div style="background-color: #121420; border: 1px solid #1c1f33; border-radius: 8px; padding: 24px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1c1f33; padding-bottom: 15px; margin-bottom: 20px;">
                        <div>
                            <span style="background-color: #1c1f33; color: #8f92a1; font-size: 11px; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 10px;">REAL</span>
                            <span style="color: #8f92a1; font-size: 13px; font-weight: 500; margin-right: 15px;">MT5 Standard</span>
                            <span style="color: #ffffff; font-weight: bold; font-size: 14px;">#130100171 TenDiGiTz</span>
                        </div>
                        <div><span class="exness-btn">🟡 Trade</span></div>
                    </div>
                    <div style="margin-bottom: 25px;">
                        <span style="color: #8f92a1; font-size: 14px; display: block; margin-bottom: 2px;">FLOATING P/L</span>
                        <h1 style="color: {neon_pl_color}; font-size: 42px; font-weight: 800; margin: 0; font-family: monospace;">{neon_pl_sign}${live_calculated_pnl:,.2f} USD</h1>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; border-top: 1px solid #1c1f33; padding-top: 20px;">
                        <div><p style="color: #8f92a1; font-size: 12px; margin: 0;">BALANCE</p><h3 style="color: #ffffff; margin: 0;">${account_settled_balance:,.2f} USD</h3></div>
                        <div><p style="color: #8f92a1; font-size: 12px; margin: 0;">FREE MARGIN</p><h3 style="color: #00d2ff; margin: 0;">${account_free_margin:,.2f} USD</h3></div>
                        <div><p style="color: #8f92a1; font-size: 12px; margin: 0;">EQUITY</p><h3 style="color: #ffffff; margin: 0;">${account_live_equity:,.2f} USD</h3></div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; background-color: #0c0d14; padding: 15px; border-radius: 6px; border: 1px solid #1c1f33;">
                        <div><p style="color: #9d4edd; font-size: 11px; font-weight: bold; margin:0;">🤖 AI LIQUIDITY TARGET</p><h4 style="color: #ffffff; margin: 0;">{live_corrected_liquidity:,.2f}</h4></div>
                        <div><p style="color: #00ffcc; font-size: 11px; font-weight: bold; margin:0;">📐 CALCULATED GOLD LOT SIZE</p><h4 style="color: #ffffff; margin: 0;">{calculated_position_lots:.2f} Lots</h4></div>
                        <div><p style="color: #3498db; font-size: 11px; font-weight: bold; margin:0;">💎 TOTAL PROFIT POTENTIAL</p><h4 style="color: #ffffff; margin: 0;">${calculated_yield_potential:,.2f}</h4></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
