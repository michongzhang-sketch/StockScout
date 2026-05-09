from __future__ import annotations

from stockscout.models import StockSnapshot
from stockscout.utils.math import clamp

PE_WEIGHT = 1.25
PB_WEIGHT = 2.5
ROE_WEIGHT = 1.4
DIVIDEND_WEIGHT = 6.0
GROWTH_WEIGHT = 3.0
LEVERAGE_WEIGHT = 12.0
VALUE_BLEND = 0.35
QUALITY_BLEND = 0.4
GROWTH_BLEND = 0.3


class FundamentalStrategy:
    def score(self, stock: StockSnapshot) -> float:
        value_score = clamp(100 - (stock.pe_ratio * PE_WEIGHT + stock.pb_ratio * PB_WEIGHT), 0.0, 100.0)
        quality_score = stock.roe * ROE_WEIGHT + stock.dividend_yield * DIVIDEND_WEIGHT
        growth_score = stock.revenue_growth * GROWTH_WEIGHT
        leverage_penalty = stock.debt_to_equity * LEVERAGE_WEIGHT
        blended_score = (
            value_score * VALUE_BLEND
            + quality_score * QUALITY_BLEND
            + growth_score * GROWTH_BLEND
            - leverage_penalty
        )
        return round(clamp(blended_score, 0.0, 100.0), 2)
