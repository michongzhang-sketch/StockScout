from __future__ import annotations

from stockscout.data_sources.config_source import ConfigDataSource
from stockscout.models import StockAnalysis, StockSnapshot, StrategyConfig
from stockscout.ranking.decision import DecisionEngine
from stockscout.risk.controller import RiskControl
from stockscout.screeners.basic import BasicScreener
from stockscout.strategies.fundamental import FundamentalStrategy
from stockscout.strategies.technical import TechnicalStrategy


class DataCollectionAgent:
    def __init__(self, source: ConfigDataSource) -> None:
        self._source = source

    def run(self) -> list[StockSnapshot]:
        return self._source.load()


class FundamentalAnalysisAgent:
    def __init__(self) -> None:
        self._strategy = FundamentalStrategy()

    def run(self, stock: StockSnapshot) -> float:
        return self._strategy.score(stock)


class TechnicalAnalysisAgent:
    def __init__(self) -> None:
        self._strategy = TechnicalStrategy()

    def run(self, stock: StockSnapshot) -> float:
        return self._strategy.score(stock)


class RiskControlAgent:
    def __init__(self) -> None:
        self._risk_control = RiskControl()

    def run(self, stock: StockSnapshot, config: StrategyConfig) -> tuple[bool, tuple[str, ...]]:
        return self._risk_control.evaluate(stock, config)


class DecisionAgent:
    def __init__(self) -> None:
        self._decision_engine = DecisionEngine()

    def run(
        self,
        stock: StockSnapshot,
        config: StrategyConfig,
        fundamental_score: float,
        technical_score: float,
        risk_flags: tuple[str, ...],
    ) -> StockAnalysis:
        return self._decision_engine.combine_scores(stock, config, fundamental_score, technical_score, risk_flags)

    def rank(self, analyses: list[StockAnalysis], config: StrategyConfig) -> list[StockAnalysis]:
        return self._decision_engine.rank(analyses, config.max_recommendations)


class ScreeningAgent:
    def __init__(self) -> None:
        self._screener = BasicScreener()

    def run(self, stocks: list[StockSnapshot], config: StrategyConfig) -> list[StockSnapshot]:
        return self._screener.filter(stocks, config)
