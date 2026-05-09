from __future__ import annotations

from stockscout.models import StockSnapshot, StrategyConfig


class BasicScreener:
    def filter(self, stocks: list[StockSnapshot], config: StrategyConfig) -> list[StockSnapshot]:
        screened: list[StockSnapshot] = []
        for stock in stocks:
            if stock.current_price <= 0 or stock.market_cap < config.min_market_cap:
                continue
            screened.append(stock)
        return screened
