from __future__ import annotations

from stockscout.models import StockSnapshot


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


class TechnicalStrategy:
    def score(self, stock: StockSnapshot) -> float:
        trend_bonus = 20 if stock.current_price >= stock.ma_50 >= stock.ma_200 else 0
        relative_strength = stock.momentum_90d * 180
        volatility_penalty = stock.volatility_90d * 120
        distance_from_trend = abs(stock.current_price - stock.ma_50) / stock.current_price * 100
        setup_score = 75 - distance_from_trend * 1.2
        return round(_clamp(setup_score + trend_bonus + relative_strength - volatility_penalty), 2)
