from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from stockscout.agents import (
    DataCollectionAgent,
    DecisionAgent,
    FundamentalAnalysisAgent,
    RiskControlAgent,
    ScreeningAgent,
    TechnicalAnalysisAgent,
)
from stockscout.data_sources.config_source import ConfigDataSource
from stockscout.models import RecommendationRow
from stockscout.reports.writer import CsvReportWriter
from stockscout.utils.config import load_strategy_config
from stockscout.utils.files import build_timestamped_output_path


class StockScoutApp:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.config_dir = repo_root / "config"
        self.output_dir = repo_root / "tmp"
        self.data_agent = DataCollectionAgent(ConfigDataSource(self.config_dir / "stocks.json"))
        self.screening_agent = ScreeningAgent()
        self.fundamental_agent = FundamentalAnalysisAgent()
        self.technical_agent = TechnicalAnalysisAgent()
        self.risk_agent = RiskControlAgent()
        self.decision_agent = DecisionAgent()
        self.writer = CsvReportWriter()

    def run(self, now: datetime | None = None, output_dir: Path | None = None) -> Path:
        runtime = now or datetime.now(timezone.utc)
        config = load_strategy_config(self.config_dir / "strategy.json")
        stocks = self.screening_agent.run(self.data_agent.run(), config)

        analyses = []
        for stock in stocks:
            fundamental_score = self.fundamental_agent.run(stock)
            technical_score = self.technical_agent.run(stock)
            is_allowed, risk_flags = self.risk_agent.run(stock, config)
            if not is_allowed:
                continue
            analyses.append(
                self.decision_agent.run(stock, config, fundamental_score, technical_score, risk_flags)
            )

        ranked = self.decision_agent.rank(analyses, config)
        rows = [
            RecommendationRow(
                current_time=runtime,
                stock_name=item.snapshot.name,
                stock_code=item.snapshot.symbol,
                current_price=item.snapshot.current_price,
                market_cap=item.snapshot.market_cap,
                recommended_buy_price=item.buy_price,
                recommended_sell_price=item.sell_price,
            )
            for item in ranked
        ]
        destination = build_timestamped_output_path(output_dir or self.output_dir, runtime)
        return self.writer.write(rows, destination)
