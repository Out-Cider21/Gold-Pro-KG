from core.smc_engine import (
    detect_bos_choch,
    detect_fvg,
    detect_liquidity_sweep,
    premium_discount,
)

from core.session_engine import current_session, quarterly_phase


def generate_confluence(df, snr_zones):
    structure = detect_bos_choch(df)
    fvgs = detect_fvg(df)
    sweep = detect_liquidity_sweep(df)
    pd_data = premium_discount(df)

    session = current_session()
    quarter = quarterly_phase()

    price = df["close"].iloc[-1]

    score = 0
    reasons = []
    active_snr = None

    if structure["bos"]:
        score += 20
        reasons.append("BOS confirmed")

    if structure["choch"]:
        score += 15
        reasons.append("CHOCH confirmed")

    if fvgs:
        score += 15
        reasons.append("Fair Value Gap imbalance present")

    if sweep != "NO CLEAR SWEEP":
        score += 20
        reasons.append(sweep)

    for zone in snr_zones:
        if zone["low"] <= price <= zone["high"]:
            active_snr = zone
            score += 20
            reasons.append(f"Price inside Malaysian SNR {zone['type']}")
            break

    if session in ["LONDON OPEN", "NEW YORK OPEN"]:
        score += 10
        reasons.append(f"Active killzone: {session}")

    if quarter in ["Q2 MANIPULATION", "Q3 DISTRIBUTION"]:
        score += 10
        reasons.append(f"Daye quarterly phase: {quarter}")

    if pd_data["zone"] in ["PREMIUM", "DISCOUNT"]:
        score += 5
        reasons.append(f"Price in {pd_data['zone']} zone")

    score = min(score, 100)

    if score >= 80:
        grade = "HIGH PROBABILITY"
    elif score >= 60:
        grade = "MEDIUM PROBABILITY"
    else:
        grade = "LOW PROBABILITY"

    return {
        "score": score,
        "grade": grade,
        "bias": structure["bias"],
        "reasons": reasons,
        "structure": structure,
        "fvgs": fvgs,
        "sweep": sweep,
        "pd": pd_data,
        "active_snr": active_snr,
        "session": session,
        "quarter": quarter,
    }
