# StockScout Architecture

## Goals

- Build a stock investment decision support system instead of a guaranteed-profit tool.
- Keep the first version deterministic and locally runnable.
- Generate a timestamped recommendation list in the repository `tmp` directory.

## Directory Layout

- `config/`: strategy thresholds and the sample stock universe
- `src/stockscout/data_sources`: raw stock input loading
- `src/stockscout/screeners`: basic candidate filtering
- `src/stockscout/strategies`: fundamental and technical scoring
- `src/stockscout/risk`: risk limits and exclusions
- `src/stockscout/ranking`: weighted score aggregation and ranking
- `src/stockscout/reports`: final CSV output
- `src/stockscout/utils`: configuration and file helpers
- `tests/`: pipeline and report validation
- `tmp/`: generated recommendation files

## Agent Responsibilities

- `DataCollectionAgent`: loads stock snapshots from configuration data
- `ScreeningAgent`: removes invalid or undersized companies
- `FundamentalAnalysisAgent`: scores value, quality, growth, and leverage
- `TechnicalAnalysisAgent`: scores trend, momentum, and volatility
- `RiskControlAgent`: blocks stocks outside the configured risk limits
- `DecisionAgent`: combines weighted scores and calculates buy/sell ranges
- `CsvReportWriter`: emits the requested report columns to a timestamped file
