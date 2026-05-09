from __future__ import annotations

from stockscout.models import StockSnapshot
from stockscout.utils.math import clamp

TREND_BONUS = 20.0
RELATIVE_STRENGTH_WEIGHT = 180.0
VOLATILITY_PENALTY_WEIGHT = 120.0
BASE_SETUP_SCORE = 75.0
TREND_DISTANCE_WEIGHT = 1.2


class TechnicalStrategy:
    def score(self, stock: StockSnapshot) -> float:
        if stock.current_price <= 0:
            return 0.0
        trend_bonus = TREND_BONUS if stock.current_price >= stock.ma_50 >= stock.ma_200 else 0.0
        relative_strength = stock.momentum_90d * RELATIVE_STRENGTH_WEIGHT
        volatility_penalty = stock.volatility_90d * VOLATILITY_PENALTY_WEIGHT
        distance_from_trend = abs(stock.current_price - stock.ma_50) / stock.current_price * 100
        setup_score = BASE_SETUP_SCORE - distance_from_trend * TREND_DISTANCE_WEIGHT
        return round(clamp(setup_score + trend_bonus + relative_strength - volatility_penalty, 0.0, 100.0), 2)
