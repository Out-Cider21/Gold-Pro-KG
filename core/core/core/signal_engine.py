def generate_signal_score(df, smc_data):

    score = 0

    if smc_data['bos']:
        score += 25

    if smc_data['fvg_detected']:
        score += 20

    if smc_data['liquidity_sweep']:
        score += 20

    if smc_data['market_structure'] == "BULLISH":
        score += 20

    score += 15

    if score > 100:
        score = 100

    return {
        "score": score,
        "bias": smc_data['market_structure']
    }
