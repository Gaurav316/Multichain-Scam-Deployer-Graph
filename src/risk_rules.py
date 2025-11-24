import pandas as pd

def score_deployer_row(row: pd.Series):
    n = row.get("n_contracts", 0)
    out = row.get("avg_out_degree", 0)

    score = 0
    if n >= 10: score += 30
    if n >= 30: score += 40
    if out >= 10: score += 30

    score = min(100, score)

    if score <= 20:
        level="Low"; label="benign_candidate"
    elif score <= 60:
        level="Medium"; label="watchlist"
    else:
        level="High"; label="high_risk_candidate"

    return {
        "risk_score": score,
        "risk_level": level,
        "risk_label": label,
    }
