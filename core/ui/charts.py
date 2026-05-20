import plotly.graph_objects as go


def build_candlestick_chart(df, smc_data):

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    ))

    fig.add_hline(
        y=smc_data['premium_zone'],
        line_dash='dash'
    )

    fig.add_hline(
        y=smc_data['discount_zone'],
        line_dash='dash'
   )

    fig.update_layout(
        paper_bgcolor='#070b14',
        plot_bgcolor='#111827',
        font=dict(color='white'),
        height=600
    )

    return fig


def build_equity_chart(df):

    fig = go.Figure()

    if not df.empty:

        equity = df['profit'].cumsum()

        fig.add_trace(go.Scatter(
            y=equity,
            mode='lines'
        ))

    fig.update_layout(
        paper_bgcolor='#070b14'
  plot_bgcolor='#111827',
        font=dict(color='white'),
        height=600
    )

    return fig
