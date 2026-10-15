"""Common utility functions."""

from pathlib import Path


def project_root():
    return Path(__file__).resolve().parents[1]


def format_number(value, decimals=1):
    return f"{value:,.{decimals}f}"


def recommendation_reason(row):
    reasons = []
    if row.get("similarity_score", 0) >= 0.7:
        reasons.append("high nutrient-profile similarity")
    elif row.get("similarity_score", 0) >= 0.4:
        reasons.append("moderate nutrient-profile similarity")
    else:
        reasons.append("available dataset match")
    reasons.append(f"diet: {row.get('Diet_Type', 'N/A')}")
    return ", ".join(reasons)
