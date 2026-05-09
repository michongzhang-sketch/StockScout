from __future__ import annotations

from stockscout.models import StockAnalysis, StockSnapshot, StrategyConfig


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


class DecisionEngine:
    def combine_scores(
        self,
        stock: StockSnapshot,
        config: StrategyConfig,
        fundamental_score: float,
        technical_score: float,
        risk_flags: tuple[str, ...],
    ) -> StockAnalysis:
        weights = config.strategy_weights
        total_score = round(
            fundamental_score * weights.get("fundamental", 0.5)
            + technical_score * weights.get("technical", 0.5),
            2,
        )
        risk_penalty = 0.0 if not risk_flags else 0.03 * len(risk_flags)
        margin_of_safety = _clamp(0.03 + max(0.0, 80 - total_score) / 500 + risk_penalty, 0.02, 0.15)
        upside_target = _clamp(0.08 + total_score / 500 + stock.dividend_yield / 100, 0.06, 0.22)
        buy_price = round(stock.current_price * (1 - margin_of_safety), 2)
        sell_price = round(stock.current_price * (1 + upside_target), 2)
        return StockAnalysis(
            snapshot=stock,
            fundamental_score=fundamental_score,
            technical_score=technical_score,
            total_score=total_score,
            buy_price=buy_price,
            sell_price=sell_price,
            risk_flags=risk_flags,
        )

    def rank(self, analyses: list[StockAnalysis], limit: int) -> list[StockAnalysis]:
        return sorted(
            analyses,
            key=lambda item: (item.total_score, item.snapshot.market_cap, item.snapshot.dividend_yield),
            reverse=True,
        )[:limit]
