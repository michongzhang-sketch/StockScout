from __future__ import annotations

from stockscout.models import StockAnalysis, StockSnapshot, StrategyConfig
from stockscout.utils.math import clamp

BASE_MARGIN_OF_SAFETY = 0.03
SCORE_TARGET = 80.0
SCORE_DISTANCE_DIVISOR = 500.0
RISK_FLAG_MARGIN_PENALTY = 0.03
MIN_MARGIN_OF_SAFETY = 0.02
MAX_MARGIN_OF_SAFETY = 0.15
BASE_UPSIDE_TARGET = 0.08
DIVIDEND_UPSIDE_DIVISOR = 100.0
MIN_UPSIDE_TARGET = 0.06
MAX_UPSIDE_TARGET = 0.22


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
        risk_penalty = 0.0 if not risk_flags else RISK_FLAG_MARGIN_PENALTY * len(risk_flags)
        margin_of_safety = clamp(
            BASE_MARGIN_OF_SAFETY + max(0.0, SCORE_TARGET - total_score) / SCORE_DISTANCE_DIVISOR + risk_penalty,
            MIN_MARGIN_OF_SAFETY,
            MAX_MARGIN_OF_SAFETY,
        )
        upside_target = clamp(
            BASE_UPSIDE_TARGET + total_score / SCORE_DISTANCE_DIVISOR + stock.dividend_yield / DIVIDEND_UPSIDE_DIVISOR,
            MIN_UPSIDE_TARGET,
            MAX_UPSIDE_TARGET,
        )
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
