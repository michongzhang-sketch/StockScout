from __future__ import annotations

from stockscout.models import StockSnapshot


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


class FundamentalStrategy:
    def score(self, stock: StockSnapshot) -> float:
        value_score = 100 - (stock.pe_ratio * 1.25 + stock.pb_ratio * 2.5)
        quality_score = stock.roe * 1.4 + stock.dividend_yield * 6
        growth_score = stock.revenue_growth * 3
        leverage_penalty = stock.debt_to_equity * 12
        return round(_clamp(value_score * 0.35 + quality_score * 0.4 + growth_score * 0.3 - leverage_penalty), 2)
