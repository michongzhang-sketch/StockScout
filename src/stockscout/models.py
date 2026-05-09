from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StockSnapshot:
    name: str
    symbol: str
    current_price: float
    market_cap: float
    pe_ratio: float
    pb_ratio: float
    dividend_yield: float
    roe: float
    revenue_growth: float
    debt_to_equity: float
    volatility_90d: float
    momentum_90d: float
    ma_50: float
    ma_200: float


@dataclass(frozen=True)
class StrategyConfig:
    max_recommendations: int
    min_market_cap: float
    max_volatility_90d: float
    max_debt_to_equity: float
    strategy_weights: dict[str, float]


@dataclass(frozen=True)
class StockAnalysis:
    snapshot: StockSnapshot
    fundamental_score: float
    technical_score: float
    total_score: float
    buy_price: float
    sell_price: float
    risk_flags: tuple[str, ...]


@dataclass(frozen=True)
class RecommendationRow:
    current_time: datetime
    stock_name: str
    stock_code: str
    current_price: float
    market_cap: float
    recommended_buy_price: float
    recommended_sell_price: float
