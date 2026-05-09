from __future__ import annotations

from stockscout.models import StockSnapshot, StrategyConfig


class RiskControl:
    def evaluate(self, stock: StockSnapshot, config: StrategyConfig) -> tuple[bool, tuple[str, ...]]:
        flags: list[str] = []
        if stock.volatility_90d > config.max_volatility_90d:
            flags.append("volatility_too_high")
        if stock.debt_to_equity > config.max_debt_to_equity:
            flags.append("debt_too_high")
        return (len(flags) == 0, tuple(flags))
