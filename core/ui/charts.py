import plotly.graph_objects as go


def build_chart(df, signal, snr_zones):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price",
        increasing_line_color="#00ffcc",
        decreasing_line_color="#ff4d6d",
    ))

    pd_data = signal["pd"]

    fig.add_hline(
        y=pd_data["range_high"],
        line_dash="dot",
        annotation_text="Range High"
    )

    fig.add_hline(
        y=pd_data["equilibrium"],
        line_dash="dash",
        annotation_text="Equilibrium"
    )

    fig.add_hline(
        y=pd_data["range_low"],
        line_dash="dot",
        annotation_text="Range Low"
    )

    for zone in snr_zones[-8:]:
        color = (
            "rgba(0,255,204,0.16)"
            if zone["type"] == "SUPPORT"
            else "rgba(255,77,109,0.16)"
        )

        fig.add_hrect(
            y0=zone["low"],
            y1=zone["high"],
            fillcolor=color,
            opacity=0.45,
            line_width=0,
            annotation_text=f"Malaysian {zone['type']}",
            annotation_position="top left",
        )

    for fvg in signal["fvgs"]:
        color = (
            "rgba(56,189,248,0.13)"
            if "BULLISH" in fvg["type"]
            else "rgba(250,204,21,0.13)"
        )

        fig.add_hrect(
            y0=fvg["low"],
            y1=fvg["high"],
            fillcolor=color,
            opacity=0.4,
            line_width=0,
            annotation_text=fvg["type"],
            annotation_position="bottom right",
        )

    fig.update_layout(
        height=620,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0b1220",
        font=dict(color="white"),
        xaxis_rangeslider_visible=False,
        yaxis=dict(gridcolor="#1f2937"),
        xaxis=dict(gridcolor="#1f2937"),
    )

    return fig


def build_equity_chart(trades):
    fig = go.Figure()

    if not trades.empty:
        chronological = trades.iloc[::-1].copy()
        chronological["equity"] = chronological["profit"].cumsum()

        fig.add_trace(go.Scatter(
            x=chronological["timestamp"],
            y=chronological["equity"],
            mode="lines+markers",
            line=dict(width=3),
            name="Equity Curve",
        ))

    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0b1220",
        font=dict(color="white"),
        yaxis=dict(gridcolor="#1f2937"),
        xaxis=dict(gridcolor="#1f2937"),
    )

    return fig
